package admin

import (
    "net/http"
    "time"	

    "angotest/config"
    "angotest/models"

    "github.com/gin-gonic/gin"
)

// ====== Estructuras para el dashboard ======

// DashboardResponse - Respuesta principal del dashboard
type DashboardResponse struct {
    Totals       DashboardTotals    `json:"totals"`
    TopTests     TopTestsLists      `json:"top_tests"`
    UserLists    UserLists          `json:"user_lists"`
}

// DashboardTotals - Totales del dashboard
type DashboardTotals struct {
    TotalUsers        int64 `json:"total_users"`
    ActiveUsers       int64 `json:"active_users"`
    TotalTests        int64 `json:"total_tests"`
    InactiveTests     int64 `json:"inactive_tests"`
    CompletedTests    int64 `json:"completed_tests"`
    InProgressTests   int64 `json:"in_progress_tests"`
    AbandonedTests    int64 `json:"abandoned_tests"`
    AdvancedTests     int64 `json:"advanced_tests"`
    IntermediateTests int64 `json:"intermediate_tests"`
    BeginnerTests     int64 `json:"beginner_tests"`
}


// TestWithCountForDashboard - Test con conteo
type TestWithCountForDashboard struct {
    ID      uint   `json:"id"`
    Title   string `json:"title"`
    Count   int64  `json:"count"`
}

// TopTestsLists - Listas de tests con diferentes métricas
type TopTestsLists struct {
    MostCompleted        []TestWithCountForDashboard `json:"most_completed"`
    MostIncomplete       []TestWithCountForDashboard `json:"most_incomplete"`
    MostAbandoned        []TestWithCountForDashboard `json:"most_abandoned"`
    LeastStartedOldest   []TestWithDate  `json:"least_started_oldest"`
    HighestAccuracy      []TestWithRate  `json:"highest_accuracy"`
    LowestAccuracy       []TestWithRate  `json:"lowest_accuracy"`
    HighestAvgTime       []TestWithTime  `json:"highest_avg_time"`
    LowestAvgTime        []TestWithTime  `json:"lowest_avg_time"`
}

// UserLists - Listas de usuarios
type UserLists struct {
    NewUsersByMonth   []UserWithCount  `json:"new_users_by_month"`
    MostActiveUsers   []UserWithCount  `json:"most_active_users"`
    LeastActiveOldest []UserWithDate   `json:"least_active_oldest"`
    RecentLogin       []UserWithDate   `json:"recent_login"`
    OldestLogin       []UserWithDate   `json:"oldest_login"`
}

// TestWithDate - Test con fecha
type TestWithDate struct {
    ID      uint      `json:"id"`
    Title   string    `json:"title"`
    AttemptCount int64     `json:"attempt_count"`
    Date    time.Time `json:"date"`	
}

// TestWithRate - Test con tasa de aciertos
type TestWithRate struct {
    ID           uint    `json:"id"`
    Title        string  `json:"title"`
    AccuracyRate float64 `json:"accuracy_rate"`
}

// TestWithTime - Test con tiempo promedio
type TestWithTime struct {
    ID          uint    `json:"id"`
    Title       string  `json:"title"`
    AvgTime     float64 `json:"avg_time"`
}

// UserWithCount - Usuario con conteo
type UserWithCount struct {
    ID       uint   `json:"id"`
    Username string `json:"username"`
    Role     string `json:"role"`
    Count    int64  `json:"count"`
}

// UserWithDate - Usuario con fecha
type UserWithDate struct {
    ID       uint      `json:"id"`
    Username string    `json:"username"`
    Role     string    `json:"role"`
    Date     time.Time `json:"date"`
}

// DashboardFilters - Filtros para el dashboard
type DashboardFilters struct {
    MonthsBack      int    `form:"months_back" binding:"omitempty,min=1,max=12"`
    Year            int    `form:"year" binding:"omitempty"`
    UseTotal        bool   `form:"use_total" binding:"omitempty"`
    Limit           int    `form:"limit" binding:"omitempty,min=1,max=50"`
}

// ====== Endpoint principal del dashboard ======
func GetAdminDashboard(c *gin.Context) {
    var filters DashboardFilters
    if err := c.ShouldBindQuery(&filters); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Configurar valores por defecto
    if filters.MonthsBack == 0 {
        filters.MonthsBack = 6 // Últimos 6 meses por defecto
    }
    if filters.Limit == 0 {
        filters.Limit = 10 // Top 10 por defecto
    }


    // Preparar la respuesta
    dashboard := DashboardResponse{
        Totals:    DashboardTotals{},
        TopTests:  TopTestsLists{},
        UserLists: UserLists{},
    }

    // Obtener todos los totales
    if err := getDashboardTotals(c, &dashboard.Totals, filters); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener totales: " + err.Error()})
        return
    }

    // Obtener listas de tests
    if err := getTopTestsLists(c, &dashboard.TopTests, filters); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener listas de tests: " + err.Error()})
        return
    }

    // Obtener listas de usuarios
    if err := getUserLists(c, &dashboard.UserLists, filters); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener listas de usuarios: " + err.Error()})
        return
    }

    c.JSON(http.StatusOK, dashboard)
}

// ====== Funciones auxiliares ======

// getDashboardTotals - Obtiene todos los totales del dashboard
func getDashboardTotals(c *gin.Context, totals *DashboardTotals, filters DashboardFilters) error {
    db := config.DB
    activeThreshold := 5 // Número de tests para considerar usuario activo

    dateCondition := getDateCondition(filters, "user")

    // 1. Total de usuarios registrados
    if err := db.Model(&models.User{}).
        Count(&totals.TotalUsers).
        Where(dateCondition).Error; err != nil {
        return err
    }

    // 2. Usuarios activos (con al menos activeThreshold tests completados)
    if err := db.Model(&models.User{}).
        Joins("JOIN results ON results.user_id = users.id AND results.status = 'completed'").
        Group("users.id").
        Having("COUNT(results.id) >= ?", activeThreshold).
        Count(&totals.ActiveUsers).Error; err != nil {
        return err
    }

    // 3. Tests desactivados
    if err := db.Model(&models.Test{}).Where("is_active = ?", false).Count(&totals.InactiveTests).Error; err != nil {
        return err
    }

    // 4-7. Tests completados, en progreso y abandonados
    var counts struct {
        Completed  int64
        InProgress int64
        Abandoned  int64
    }
    
    dateCondition = getDateCondition(filters, "result")

    if err := db.Model(&models.Result{}).
        Table("results AS r").
        Select(`
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'in_progress' AND updated_at >= NOW() - INTERVAL '30 DAY' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status IN ('abandoned', 'in_progress') AND updated_at < NOW() - INTERVAL '30 DAY' THEN 1 ELSE 0 END) as abandoned
        `).
        Where(dateCondition).
        Scan(&counts).Error; err != nil {
        return err
    }
    
    totals.CompletedTests = counts.Completed
    totals.InProgressTests = counts.InProgress
    totals.AbandonedTests = counts.Abandoned

    dateCondition = getDateCondition(filters, "test")

    // 8-10. Tests por nivel
    if err := db.Model(&models.Test{}).Where(dateCondition + " AND level = ?", "Avanzado").Count(&totals.AdvancedTests).Error; err != nil {
        return err
    }

    if err := db.Model(&models.Test{}).Where(dateCondition + " AND level = ?", "Intermedio").Count(&totals.IntermediateTests).Error; err != nil {
        return err
    }

    if err := db.Model(&models.Test{}).Where(dateCondition + " AND level = ?", "Principiante").Count(&totals.BeginnerTests).Error; err != nil {
        return err
    }

    // 11. Total de tests
    if err := db.Model(&models.Test{}).Where(dateCondition).Count(&totals.TotalTests).Error; err != nil {
        return err
    }

    return nil
}

// getTopTestsLists - Obtiene las listas de tests
func getTopTestsLists(c *gin.Context, lists *TopTestsLists, filters DashboardFilters) error {
    // Calcular fechas límite según filtros
    dateCondition := getDateCondition(filters, "result")

    // 1. Tests con más completados
    if err := getMostCompletedTests(&lists.MostCompleted, dateCondition, filters.Limit); err != nil {
        return err
    }

    // 2. Tests con más incompletos (en progreso)
    if err := getMostIncompleteTests(&lists.MostIncomplete, dateCondition, filters.Limit); err != nil {
        return err
    }

    // 3. Tests con más abandonados (updated_at > 30 días)
    if err := getMostAbandonedTests(&lists.MostAbandoned, filters.Limit); err != nil {
        return err
    }

    // 4. Tests menos iniciados y más antiguos
    if err := getLeastStartedOldestTests(&lists.LeastStartedOldest, dateCondition, filters.Limit); err != nil {
        return err
    }

    // 5. Tests con mayor tasa de aciertos
    if err := getTestsByAccuracy(&lists.HighestAccuracy, dateCondition, filters.Limit, true); err != nil {
        return err
    }

    // 6. Tests con menor tasa de aciertos
    if err := getTestsByAccuracy(&lists.LowestAccuracy, dateCondition, filters.Limit, false); err != nil {
        return err
    }

    // 7. Tests con mayor tiempo promedio
    if err := getTestsByAvgTime(&lists.HighestAvgTime, dateCondition, filters.Limit, true); err != nil {
        return err
    }

    // 8. Tests con menor tiempo promedio
    if err := getTestsByAvgTime(&lists.LowestAvgTime, dateCondition, filters.Limit, false); err != nil {
        return err
    }

    return nil
}

// getUserLists - Obtiene las listas de usuarios
func getUserLists(c *gin.Context, lists *UserLists, filters DashboardFilters) error {
    // Calcular fechas límite según filtros
    dateCondition := getDateCondition(filters, "user")

    // 1. Nuevos usuarios por mes
    if err := getNewUsersByMonth(&lists.NewUsersByMonth, dateCondition, filters.Limit); err != nil {
        return err
    }

    // 2. Usuarios más activos
    if err := getMostActiveUsers(&lists.MostActiveUsers, dateCondition, filters.Limit); err != nil {
        return err
    }

    // 3. Usuarios menos activos y más antiguos
    if err := getLeastActiveOldestUsers(&lists.LeastActiveOldest, filters.Limit); err != nil {
        return err
    }

    // 4. Usuarios con login más reciente
    if err := getUsersByLoginDate(&lists.RecentLogin, filters.Limit, true); err != nil {
        return err
    }

    // 5. Usuarios con login más antiguo
    if err := getUsersByLoginDate(&lists.OldestLogin, filters.Limit, false); err != nil {
        return err
    }

    return nil
}

// ====== Funciones específicas para cada métrica ======

func getMostCompletedTests(results *[]TestWithCountForDashboard, dateCondition string, limit int) error {
    query := `
        SELECT 
            t.id,
            t.title,
            COUNT(r.id) as count
        FROM tests t
        LEFT JOIN results r ON r.test_id = t.id AND r.status = 'completed'
    `
    
    if dateCondition != "" {
        query += " WHERE " + dateCondition
    }
    
    query += `
        GROUP BY t.id, t.title
        ORDER BY count DESC
        LIMIT ?
    `
	return config.DB.Raw(query, limit).Scan(results).Error
}

func getMostIncompleteTests(results *[]TestWithCountForDashboard, dateCondition string, limit int) error {
    query := `
        SELECT 
            t.id,
            t.title,
            COUNT(r.id) as count
        FROM tests t
        LEFT JOIN results r ON r.test_id = t.id AND r.status = 'in_progress'
    `
    
    if dateCondition != "" {
        query += " WHERE " + dateCondition
    }
    
    query += `
        GROUP BY t.id, t.title
        ORDER BY count DESC
        LIMIT ?
    `
    
    return config.DB.Raw(query, limit).Scan(results).Error
}

func getMostAbandonedTests(results *[]TestWithCountForDashboard, limit int) error {
    thirtyDaysAgo := time.Now().AddDate(0, 0, -30)
    
    query := `
        SELECT 
            t.id,
            t.title,
            COUNT(r.id) as count
        FROM tests t
        LEFT JOIN results r ON r.test_id = t.id 
            AND r.status IN ('abandoned', 'in_progress')
            AND r.updated_at < ?
        GROUP BY t.id, t.title
        ORDER BY count DESC
        LIMIT ?
    `
    
    return config.DB.Raw(query, thirtyDaysAgo, limit).Scan(results).Error
}

func getLeastStartedOldestTests(results *[]TestWithDate, dateCondition string, limit int) error {
    baseQuery := `
        SELECT 
            t.id,
            t.title,
            t.created_at as date,
            COUNT(r.id) as attempt_count
        FROM tests t
        LEFT JOIN results r ON r.test_id = t.id
    `
    
    if dateCondition != "" {
        baseQuery += " WHERE " + dateCondition
    }
    
    query := baseQuery + `
        GROUP BY t.id, t.title, t.created_at
        ORDER BY COUNT(r.id) ASC, t.created_at ASC
        LIMIT ?
    `    
    return config.DB.Raw(query, limit).Scan(results).Error
}

func getTestsByAccuracy(results *[]TestWithRate, dateCondition string, limit int, highest bool) error {
    orderBy := "DESC"
    if !highest {
        orderBy = "ASC"
    }
    
    baseQuery := `
        SELECT 
            t.id,
            t.title,
            CASE 
                WHEN COUNT(r.id) = 0 THEN 0
                ELSE AVG(r.correct_answers * 100.0 / (r.correct_answers + r.wrong_answers))
            END as accuracy_rate
        FROM tests t
        LEFT JOIN results r ON r.test_id = t.id AND r.status = 'completed'
    `
    
    if dateCondition != "" {
        baseQuery += " WHERE " + dateCondition
    }
    
    query := baseQuery + `
        GROUP BY t.id, t.title
        HAVING COUNT(r.id) > 0
        ORDER BY accuracy_rate ` + orderBy + `
        LIMIT ?
    `
    
    return config.DB.Raw(query, limit).Scan(results).Error
}

func getTestsByAvgTime(results *[]TestWithTime, dateCondition string, limit int, highest bool) error {
    orderBy := "DESC"
    if !highest {
        orderBy = "ASC"
    }
    
    baseQuery := `
        SELECT 
            t.id,
            t.title,
            AVG(r.time_taken) as avg_time
        FROM tests t
        LEFT JOIN results r ON r.test_id = t.id AND r.status = 'completed'
    `
    
    if dateCondition != "" {
        baseQuery += " WHERE " + dateCondition
    }
    
    query := baseQuery + `
        GROUP BY t.id, t.title
        HAVING COUNT(r.id) > 0
        ORDER BY avg_time ` + orderBy + `
        LIMIT ?
    `
    
    return config.DB.Raw(query, limit).Scan(results).Error
}

func getNewUsersByMonth(results *[]UserWithCount, dateCondition string, limit int) error {
    baseQuery := `
        SELECT 
            u.id,
            u.username,
            u.role,
            DATE_TRUNC('month', u.registered_at) as month,
            COUNT(*) as count
        FROM users u
    `
    
    if dateCondition != "" {
        baseQuery += " WHERE " + dateCondition
    }
    
    query := baseQuery + `
        GROUP BY u.id, u.username, u.role, DATE_TRUNC('month', u.registered_at)
        ORDER BY month DESC, count DESC
        LIMIT ?
    `
    
    return config.DB.Raw(query, limit).Scan(results).Error
}

func getMostActiveUsers(results *[]UserWithCount, dateCondition string, limit int) error {
    baseQuery := `
        SELECT 
            u.id,
            u.username,
            u.role,
            COUNT(r.id) as count
        FROM users u
        LEFT JOIN results r ON r.user_id = u.id AND r.status = 'completed'
    `
    
    if dateCondition != "" {
        baseQuery += " WHERE " + dateCondition
    }
    
    query := baseQuery + `
        GROUP BY u.id, u.username
        HAVING COUNT(r.id) > 0
        ORDER BY count DESC
        LIMIT ?
    `
    
    return config.DB.Raw(query, limit).Scan(results).Error
}

func getLeastActiveOldestUsers(results *[]UserWithDate, limit int) error {
    query := `
        SELECT 
            u.id,
            u.username,
            u.role,
            u.registered_at as date
        FROM users u
        LEFT JOIN results r ON r.user_id = u.id AND r.status = 'completed'
        GROUP BY u.id, u.username, u.role, u.registered_at
        HAVING COUNT(r.id) = 0
        ORDER BY u.registered_at ASC
        LIMIT ?
    `
    
    return config.DB.Raw(query, limit).Scan(results).Error
}

func getUsersByLoginDate(results *[]UserWithDate, limit int, recent bool) error {
    orderBy := "DESC"
    if !recent {
        orderBy = "ASC"
    }
    
    query := `
        SELECT 
            u.id,
            u.username,
            u.role,
            u.login_at as date
        FROM users u
        WHERE u.login_at IS NOT NULL
        ORDER BY u.login_at ` + orderBy + `
        LIMIT ?
    `
    
    return config.DB.Raw(query, limit).Scan(results).Error
}

// getDateCondition - Genera la condición WHERE basada en los filtros
func getDateCondition(filters DashboardFilters, model string) string {
    if filters.UseTotal {
        return ""
    }

	if model == "" {
		model = "test"
	}
    
    if filters.Year > 0 {
        startDate := time.Date(filters.Year, 1, 1, 0, 0, 0, 0, time.UTC)
        endDate := time.Date(filters.Year+1, 1, 1, 0, 0, 0, 0, time.UTC)
		if model == "test" {
        	return "created_at >= '" + startDate.Format("2006-01-02") + "' AND created_at < '" + endDate.Format("2006-01-02") + "'"
        } else if model == "user" {
            return "registered_at >= '" + startDate.Format("2006-01-02") + "' AND registered_at < '" + endDate.Format("2006-01-02") + "'"
		} else { //result
			return "r.updated_at >= '" + startDate.Format("2006-01-02") + "' AND r.updated_at < '" + endDate.Format("2006-01-02") + "'"
		}
    }
    
    if filters.MonthsBack > 0 {
        startDate := time.Now().AddDate(0, -filters.MonthsBack, 0)
		if model == "test" {
        	return "created_at >= '" + startDate.Format("2006-01-02") + "'"
		} else if model == "user" {
			return "registered_at >= '" + startDate.Format("2006-01-02") + "'"
		} else { //result
			return "r.updated_at >= '" + startDate.Format("2006-01-02") + "'"
		}
    }
    
    return ""
}


// ====== Endpoint separado para estadísticas detalladas de tests ======
func GetTestDetailedStats(c *gin.Context) {
    testID := c.Param("test_id")
    
    var stats struct {
        TotalAttempts     int64   `json:"total_attempts"`
        CompletedAttempts int64   `json:"completed_attempts"`
        InProgressAttempts int64  `json:"in_progress_attempts"`
        AvgAccuracy       float64 `json:"avg_accuracy"`
        AvgTime           float64 `json:"avg_time"`
        CompletionRate    float64 `json:"completion_rate"`
        DifficultyLevel   string  `json:"difficulty_level"`
        TestTitle         string  `json:"test_title"`
        TopicHierarchy    struct {
            MainTopic     string `json:"main_topic"`
            SubTopic      string `json:"sub_topic"`
            SpecificTopic string `json:"specific_topic"`
        } `json:"topic_hierarchy"`
    }
    
    // Obtener información básica del test
    var test models.Test
    if err := config.DB.First(&test, testID).Error; err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "Test no encontrado"})
        return
    }
    
    stats.TestTitle = test.Title
    stats.TopicHierarchy.MainTopic = test.MainTopic
    stats.TopicHierarchy.SubTopic = test.SubTopic
    stats.TopicHierarchy.SpecificTopic = test.SpecificTopic
    stats.DifficultyLevel = test.Level
    
    // Obtener estadísticas de resultados
    var resultStats struct {
        TotalAttempts     int64
        CompletedAttempts int64
        InProgressAttempts int64
        AvgCorrectAnswers float64
        AvgWrongAnswers   float64
        AvgTimeTaken      float64
    }
    
    err := config.DB.Model(&models.Result{}).
        Select(`
            COUNT(*) as total_attempts,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_attempts,
            SUM(CASE WHEN status = 'in_progress' AND updated_at >= NOW() - INTERVAL '30 DAY' THEN 1 ELSE 0 END) as in_progress_attempts,
            AVG(correct_answers) as avg_correct_answers,
            AVG(wrong_answers) as avg_wrong_answers,
            AVG(time_taken) as avg_time_taken
        `).
        Where("test_id = ?", testID).
        Scan(&resultStats).Error
    
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener estadísticas: " + err.Error()})
        return
    }
    
    stats.TotalAttempts = resultStats.TotalAttempts
    stats.CompletedAttempts = resultStats.CompletedAttempts
    stats.InProgressAttempts = resultStats.InProgressAttempts
    
    // Calcular tasas y promedios
    if resultStats.TotalAttempts > 0 {
        stats.CompletionRate = float64(resultStats.CompletedAttempts) / float64(resultStats.TotalAttempts) * 100
    }
    
    if resultStats.CompletedAttempts > 0 {
        stats.AvgAccuracy = resultStats.AvgCorrectAnswers / (resultStats.AvgCorrectAnswers + resultStats.AvgWrongAnswers) * 100
        stats.AvgTime = resultStats.AvgTimeTaken
    }
    
    c.JSON(http.StatusOK, stats)
}

// ====== Endpoint para estadísticas de usuarios ======
func GetUserDetailedStats(c *gin.Context) {
    userID := c.Param("user_id")
    
    var stats struct {
        UserInfo struct {
            Username   string    `json:"username"`
            Email      string    `json:"email"`
            RegisteredAt  time.Time `json:"registered_at"`
            LastLogin  time.Time `json:"last_login"`
            Role       string    `json:"role"`
        } `json:"user_info"`
        TestStats struct {
            TotalTests         int64   `json:"total_tests"`
            CompletedTests     int64   `json:"completed_tests"`
            InProgressTests    int64   `json:"in_progress_tests"`
            AbandonedTests     int64   `json:"abandoned_tests"`
            AvgAccuracy        float64 `json:"avg_accuracy"`
            AvgTimePerTest     float64 `json:"avg_time_per_test"`
            FavoriteTopic      string  `json:"favorite_topic"`
            FavoriteLevel      string  `json:"favorite_level"`
        } `json:"test_stats"`
        RecentActivity []struct {
            TestTitle  string    `json:"test_title"`
            Status     string    `json:"status"`
            Accuracy   float64   `json:"accuracy"`
            TimeTaken  int       `json:"time_taken"`
            StartedAt  time.Time `json:"started_at"`
        } `json:"recent_activity"`
    }
    
    // Obtener información del usuario
    var user models.User
    if err := config.DB.First(&user, userID).Error; err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "Usuario no encontrado"})
        return
    }
    
    stats.UserInfo.Username = user.Username
    stats.UserInfo.Email = user.Email
    stats.UserInfo.RegisteredAt = user.RegisteredAt
    stats.UserInfo.LastLogin = user.LoginAt
    stats.UserInfo.Role = user.Role
    
    // Obtener estadísticas de resultados del usuario
    var resultStats struct {
        TotalResults    int64
        Completed       int64
        InProgress      int64
        Abandoned       int64
        AvgCorrect      float64
        AvgWrong        float64
        AvgTime         float64
    }
    
    err := config.DB.Model(&models.Result{}).
        Select(`
            COUNT(*) as total_results,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
            SUM(CASE WHEN status = 'in_progress' AND updated_at >= NOW() - INTERVAL '30 DAY' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status IN ('abandoned', 'in_progress') AND updated_at < NOW() - INTERVAL '30 DAY' THEN 1 ELSE 0 END) as abandoned,
            AVG(correct_answers) as avg_correct,
            AVG(wrong_answers) as avg_wrong,
            AVG(time_taken) as avg_time
        `).
        Where("user_id = ?", userID).
        Scan(&resultStats).Error
    
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener estadísticas: " + err.Error()})
        return
    }
    
    stats.TestStats.TotalTests = resultStats.TotalResults
    stats.TestStats.CompletedTests = resultStats.Completed
    stats.TestStats.InProgressTests = resultStats.InProgress
    stats.TestStats.AbandonedTests = resultStats.Abandoned
    
    if resultStats.Completed > 0 {
        stats.TestStats.AvgAccuracy = resultStats.AvgCorrect / (resultStats.AvgCorrect + resultStats.AvgWrong) * 100
        stats.TestStats.AvgTimePerTest = resultStats.AvgTime
    }
    
    // Obtener tema favorito
    var favoriteTopic struct {
        MainTopic string
        Count     int64
    }
    
    config.DB.Model(&models.Result{}).
        Select("tests.main_topic, COUNT(*) as count").
        Joins("JOIN tests ON tests.id = results.test_id").
        Where("results.user_id = ?", userID).
        Group("tests.main_topic").
        Order("count DESC").
        Limit(1).
        Scan(&favoriteTopic)
    
    stats.TestStats.FavoriteTopic = favoriteTopic.MainTopic
    
    // Obtener nivel favorito
    var favoriteLevel struct {
        Level string
        Count int64
    }
    
    config.DB.Model(&models.Result{}).
        Select("tests.level, COUNT(*) as count").
        Joins("JOIN tests ON tests.id = results.test_id").
        Where("results.user_id = ?", userID).
        Group("tests.level").
        Order("count DESC").
        Limit(1).
        Scan(&favoriteLevel)
    
    stats.TestStats.FavoriteLevel = favoriteLevel.Level
    
    // Obtener actividad reciente (últimos 10 tests)
    config.DB.Model(&models.Result{}).
        Select(`
            tests.title as test_title,
            results.status,
            CASE 
                WHEN results.status = 'completed' THEN 
                    results.correct_answers * 100.0 / (results.correct_answers + results.wrong_answers)
                ELSE 0 
            END as accuracy,
            results.time_taken,
            results.started_at
        `).
        Joins("JOIN tests ON tests.id = results.test_id").
        Where("results.user_id = ?", userID).
        Order("results.started_at DESC").
        Limit(10).
        Scan(&stats.RecentActivity)
    
    c.JSON(http.StatusOK, stats)
}