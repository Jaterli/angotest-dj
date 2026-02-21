package user

import (
	"net/http"
	"strconv"

	"angotest/config"
	"angotest/services"
	"angotest/types"

	"github.com/gin-gonic/gin"
)

// rankingQueries - Contiene todas las queries de rankings
var rankingQueries = map[string]string{
	"top_by_tests": `
		SELECT 
			u.id as user_id,
			u.username,
			COUNT(DISTINCT r.test_id) as value,
			ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT r.test_id) DESC) as rank
		FROM users u
		LEFT JOIN results r ON u.id = r.user_id AND r.status = 'completed'
		GROUP BY u.id, u.username
		HAVING COUNT(DISTINCT r.test_id) > ?
		ORDER BY rank
		LIMIT ?`,
		
	"top_by_level": `
		SELECT 
			u.id as user_id,
			u.username,
			COUNT(DISTINCT r.test_id) as value,
			ROW_NUMBER() OVER (ORDER BY COUNT(DISTINCT r.test_id) DESC) as rank
		FROM users u
		LEFT JOIN results r ON u.id = r.user_id AND r.status = 'completed'
		LEFT JOIN tests t ON r.test_id = t.id AND t.level = ?
		WHERE t.level IS NOT NULL
		GROUP BY u.id, u.username
		HAVING COUNT(DISTINCT r.test_id) > ?
		ORDER BY rank
		LIMIT ?`,

	"top_by_levels_accuracy": `
		WITH first_attempt AS (
			SELECT
				r.user_id,
				r.test_id,
				r.correct_answers,
				r.wrong_answers,
				ROW_NUMBER() OVER (
					PARTITION BY r.user_id, r.test_id
					ORDER BY r.updated_at ASC
				) AS attempt_num
			FROM results r
			WHERE r.status = 'completed'
		)
		SELECT 
			u.id AS user_id,
			u.username,
			CASE 
				WHEN SUM(fa.correct_answers + fa.wrong_answers) > 0
				THEN (SUM(fa.correct_answers) * 100.0)
					/ SUM(fa.correct_answers + fa.wrong_answers)
				ELSE 0
			END AS value,
			ROW_NUMBER() OVER (
				ORDER BY
					CASE 
						WHEN SUM(fa.correct_answers + fa.wrong_answers) > 0
						THEN (SUM(fa.correct_answers) * 100.0)
							/ SUM(fa.correct_answers + fa.wrong_answers)
						ELSE 0
					END DESC
			) AS rank
		FROM users u
		JOIN first_attempt fa 
			ON fa.user_id = u.id
			AND fa.attempt_num = 1
		JOIN tests t 
			ON fa.test_id = t.id
		WHERE t.level = ?
		GROUP BY u.id, u.username
		HAVING SUM(fa.correct_answers + fa.wrong_answers) > 0 AND COUNT(DISTINCT fa.test_id) >= ?
		ORDER BY rank
		LIMIT ?
	`,
}

// getTopByMetric - Función genérica para obtener tops
func getTopByMetric(metric string, args ...interface{}) []types.RankingItem {
	var items []types.RankingItem
	if query, exists := rankingQueries[metric]; exists {
		config.DB.Raw(query, args...).Scan(&items)
	}
	return items
}

// getTopByAvgTime - Obtiene top por tiempo promedio
func getTopByAvgTime(attemptType string, limit int) []types.RankingItem {
	var items []types.RankingItem
	
	query := `
		WITH user_stats AS (
			SELECT 
				r.user_id,
				SUM(r.time_taken) as total_time,
				SUM(r.correct_answers + r.wrong_answers) as total_questions_answered,
				COUNT(DISTINCT r.test_id) as tests_count
			FROM results r
			WHERE r.status = 'completed'
			`
	
	if attemptType == "first" {
		query += `
			AND (r.user_id, r.test_id, r.updated_at) IN (
				SELECT 
					user_id,
					test_id,
					MIN(updated_at) as first_updated
				FROM results 
				WHERE status = 'completed'
				GROUP BY user_id, test_id
			)`
	}
	
	query += `
			GROUP BY r.user_id
			HAVING SUM(r.correct_answers + r.wrong_answers) > 0 
				AND COUNT(DISTINCT r.test_id) >= ?
		)
		SELECT 
			u.id as user_id,
			u.username,
			CASE 
				WHEN us.total_questions_answered > 0 
				THEN ROUND(us.total_time * 1.0 / us.total_questions_answered, 2)
				ELSE 0 
			END as value,
			ROW_NUMBER() OVER (ORDER BY 
				CASE 
					WHEN us.total_questions_answered > 0 
					THEN us.total_time * 1.0 / us.total_questions_answered
					ELSE 0 
				END ASC
			) as rank
		FROM users u
		INNER JOIN user_stats us ON u.id = us.user_id
		ORDER BY rank
		LIMIT ?`
	
	config.DB.Raw(query, services.MinTestsForRanking, limit).Scan(&items)
	return items
}

// getTopByAccuracy - Obtiene top por precisión
func getTopByAccuracy(attemptType string, limit int) []types.RankingItem {
	var items []types.RankingItem
	
	query := `
		WITH user_stats AS (
			SELECT 
				r.user_id,
				SUM(r.correct_answers) as total_correct,
				SUM(r.correct_answers + r.wrong_answers) as total_questions_answered,
				COUNT(DISTINCT r.test_id) as tests_count
			FROM results r
			WHERE r.status = 'completed'
			`
	
	if attemptType == "first" {
		query += `
			AND (r.user_id, r.test_id, r.updated_at) IN (
				SELECT 
					user_id,
					test_id,
					MIN(updated_at) as first_updated
				FROM results 
				WHERE status = 'completed'
				GROUP BY user_id, test_id
			)`
	}
	
	query += `
			GROUP BY r.user_id
			HAVING SUM(r.correct_answers + r.wrong_answers) > 0 
				AND COUNT(DISTINCT r.test_id) >= ?
		)
		SELECT 
			u.id as user_id,
			u.username,
			CASE 
				WHEN us.total_questions_answered > 0 
				THEN ROUND((us.total_correct * 100.0) / us.total_questions_answered, 2)
				ELSE 0 
			END as value,
			ROW_NUMBER() OVER (ORDER BY 
				CASE 
					WHEN us.total_questions_answered > 0 
					THEN (us.total_correct * 100.0) / us.total_questions_answered
					ELSE 0 
				END DESC
			) as rank
		FROM users u
		INNER JOIN user_stats us ON u.id = us.user_id
		ORDER BY rank
		LIMIT ?`
	
	config.DB.Raw(query, services.MinTestsForRanking, limit).Scan(&items)
	return items
}

// getTopByQuestionsAnswered - Obtiene top por preguntas respondidas
func getTopByQuestionsAnswered(attemptType string, limit int) []types.RankingItem {
	var items []types.RankingItem
	
	query := `
		WITH user_stats AS (
			SELECT 
				r.user_id,
				SUM(r.correct_answers + r.wrong_answers) as total_questions_answered,
				COUNT(DISTINCT r.test_id) as tests_count
			FROM results r
			WHERE r.status = 'completed'
			`
	
	if attemptType == "first" {
		query += `
			AND (r.user_id, r.test_id, r.updated_at) IN (
				SELECT 
					user_id,
					test_id,
					MIN(updated_at) as first_updated
				FROM results 
				WHERE status = 'completed'
				GROUP BY user_id, test_id
			)`
	}
	
	query += `
			GROUP BY r.user_id
			HAVING SUM(r.correct_answers + r.wrong_answers) > 0 
				AND COUNT(DISTINCT r.test_id) >= ?
		)
		SELECT 
			u.id as user_id,
			u.username,
			COALESCE(us.total_questions_answered, 0) as value,
			ROW_NUMBER() OVER (ORDER BY COALESCE(us.total_questions_answered, 0) DESC) as rank
		FROM users u
		INNER JOIN user_stats us ON u.id = us.user_id
		ORDER BY rank
		LIMIT ?`
	
	config.DB.Raw(query, services.MinTestsForRanking, limit).Scan(&items)
	return items
}

// initializeRankingsResponse - Inicializa la respuesta de rankings
func initializeRankingsResponse() types.RankingsResponse {
	return types.RankingsResponse{
		TopByTests: []types.RankingItem{},
		TopByAvgTimeTakenPerQuestion: types.AttemptRankings{
			AllAttempts:  []types.RankingItem{},
			FirstAttempt: []types.RankingItem{},
		},
		TopByAccuracy: types.AttemptRankings{
			AllAttempts:  []types.RankingItem{},
			FirstAttempt: []types.RankingItem{},
		},
		TopByQuestionsAnswered: types.AttemptRankings{
			AllAttempts:  []types.RankingItem{},
			FirstAttempt: []types.RankingItem{},
		},
		TopByLevels:         make(map[string][]types.RankingItem),
		TopByLevelsAccuracy: make(map[string][]types.RankingItem),

		CurrentUserPosition: types.CurrentUserPositions{
			Levels: make(map[string]types.LevelRanking),},

		CommunityAverages: types.CommunityAverages{
			Levels: make(map[string]types.CommunityLevelAverages),
		},
	}
}

// populateUserPosition - Llena la posición del usuario
func populateUserPosition(response *types.RankingsResponse, userID uint, statsService *services.DataService) {
	positions, err := statsService.GetUserAllRankingPositions(userID)
	if err == nil {
		response.CurrentUserPosition = positions
	}
}

// populateCommunityAverages - Llena los promedios de comunidad
func populateCommunityAverages(response *types.RankingsResponse, statsService *services.DataService) {
	if communityAverages, err := statsService.GetCommunityAverages(); err == nil {
		response.CommunityAverages = communityAverages
	}
}

// getLimitFromQuery - Obtiene el límite desde los parámetros de consulta
func getLimitFromQuery(c *gin.Context) int {
	limit := 10
	if limitStr := c.Query("limit"); limitStr != "" {
		if l, err := strconv.Atoi(limitStr); err == nil && l > 0 && l <= 50 {
			limit = l
		}
	}
	return limit
}

// GetRankings - Obtiene solo rankings y posición del usuario
func GetRankings(c *gin.Context) {
	userID := getUserIDFromContext(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "no autorizado"})
		return
	}

	response := initializeRankingsResponse()
	statsService := services.DataService{}
	limit := getLimitFromQuery(c)

	// Obtener todos los tops
	response.TopByTests = getTopByMetric("top_by_tests", services.MinTestsForRanking, limit)
	
	response.TopByAvgTimeTakenPerQuestion.AllAttempts = getTopByAvgTime("all", limit)
	response.TopByAvgTimeTakenPerQuestion.FirstAttempt = getTopByAvgTime("first", limit)
	
	response.TopByAccuracy.AllAttempts = getTopByAccuracy("all", limit)
	response.TopByAccuracy.FirstAttempt = getTopByAccuracy("first", limit)
	
	response.TopByQuestionsAnswered.AllAttempts = getTopByQuestionsAnswered("all", limit)
	response.TopByQuestionsAnswered.FirstAttempt = getTopByQuestionsAnswered("first", limit)

	// Obtener rankings por niveles
	levels := []string{"Principiante", "Intermedio", "Avanzado"}
	for _, level := range levels {
		items := getTopByMetric("top_by_level", level, services.MinTestsForRanking, limit)
		response.TopByLevels[level] = items
		
		itemsAcc := getTopByMetric("top_by_levels_accuracy", level, services.MinTestsForRanking, limit)
		response.TopByLevelsAccuracy[level] = itemsAcc
	}

	// Obtener posición del usuario
	populateUserPosition(&response, userID, &statsService)

	// Obtener promedios de comunidad
	populateCommunityAverages(&response, &statsService)

	response.MinTestsForRanking = services.MinTestsForRanking

	c.JSON(http.StatusOK, response)
}