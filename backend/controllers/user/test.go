package user

import (
	"net/http"
    "math"

	"angotest/config"
	"angotest/models"

	"github.com/gin-gonic/gin"
)


// ====== Obtener test por ID con preguntas y respuestas ======
func GetTestByID(c *gin.Context) {
	id := c.Param("test_id")

	var test models.Test
	if err := config.DB.Preload("Questions.Answers").First(&test, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "test no encontrado"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"test": test})
}


type TestWithStatusResponse struct {
	models.Test
	TotalQuestions int        `json:"total_questions"`
}

// ====== Obtener tests NO INICIADOS con filtros y paginación ======
type NotStartedTestsResponse struct {
    Tests         []TestWithStatusResponse `json:"tests"`
    TotalTests    int64                    `json:"total_tests"`
    TotalPages    int                      `json:"total_pages"`
    CurrentPage   int                      `json:"current_page"`
    PageSize      int                      `json:"page_size"`
    HasMore       bool                     `json:"has_more"`
	MainTopics    []string                 `json:"main_topics"`    
}

type NotStartedTestsFilter struct {
    Page      int    `form:"page" binding:"omitempty,min=1"`
    PageSize  int    `form:"page_size" binding:"omitempty,min=1,max=50"`
    MainTopic string `form:"main_topic" binding:"omitempty"`
    Level     string `form:"level" binding:"omitempty"`
    SortBy    string `form:"sort_by" binding:"omitempty,oneof=test_title test_created_at test_updated_at test_level questions"`
    SortOrder string `form:"sort_order" binding:"omitempty,oneof=asc desc"`
}

// Modificar la estructura de stats para incluir total por nivel
type NotStartedTestsStats struct {
    TotalTests            int64           `json:"total_tests"`
    TotalFilteredTests    int64           `json:"total_filtered_tests"`
    TotalByLevel          map[string]int64 `json:"total_by_level"`  // Nuevo campo
}

func GetNotStartedTests(c *gin.Context) {
    userIDIfc, exists := c.Get("user_id")
    if !exists {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "usuario no autenticado"})
        return
    }
    userID, ok := userIDIfc.(uint)
    if !ok {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "user_id inválido"})
        return
    }

    var filter NotStartedTestsFilter
    if err := c.ShouldBindQuery(&filter); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Valores por defecto
    if filter.Page == 0 {
        filter.Page = 1
    }
    if filter.PageSize == 0 {
        filter.PageSize = 10
    }

    // Obtener IDs de tests donde el usuario tiene resultados (in_progress o completed)
    var userResultTestIDs []uint
    config.DB.Model(&models.Result{}).
        Select("DISTINCT(test_id)").
        Where("user_id = ?", userID).
        Find(&userResultTestIDs)

    // Construir consulta base excluyendo tests donde el usuario tiene resultados
    query := config.DB.Model(&models.Test{})

    // Si el usuario tiene resultados en algunos tests, excluirlos
    if len(userResultTestIDs) > 0 {
        query = query.Where("tests.is_active = true AND tests.id NOT IN (?)", userResultTestIDs)
    }

    // Obtener totales por nivel ANTES de aplicar filtros de topic/level
    var levelCounts []struct {
        Level string
        Count int64
    }
    
    // Crear una copia de la query base para contar por nivel
    levelQuery := config.DB.Model(&models.Test{})
    if len(userResultTestIDs) > 0 {
        levelQuery = levelQuery.Where("tests.is_active = true AND tests.id NOT IN (?)", userResultTestIDs)
    }
    
    // Contar por nivel
    err := levelQuery.
        Select("level, COUNT(*) as count").
        Group("level").
        Find(&levelCounts).Error
    
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al obtener conteo por nivel: " + err.Error()})
        return
    }
    
    // Convertir a mapa
    totalByLevel := make(map[string]int64)
    var totalTests int64 = 0
    
    for _, lc := range levelCounts {
        totalByLevel[lc.Level] = lc.Count
        totalTests += lc.Count
    }

    // Aplicar filtros adicionales (topic/level) a la consulta principal
    if filter.MainTopic != "" && filter.MainTopic != "all" {
        query = query.Where("tests.main_topic = ?", filter.MainTopic)
    }
    if filter.Level != "" && filter.Level != "all" {
        query = query.Where("tests.level = ?", filter.Level)
    }

    // Contar total con filtros (sin paginación)
    var TotalFilteredTests int64
    if err := query.Count(&TotalFilteredTests).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al contar tests con filtros: " + err.Error()})
        return
    }

    // Calcular paginación
    offset := (filter.Page - 1) * filter.PageSize
    totalPages := 0
    if TotalFilteredTests > 0 {
        totalPages = int(math.Ceil(float64(TotalFilteredTests) / float64(filter.PageSize)))
    }

    // Determinar ordenación
    orderClause := "tests.created_at DESC" // Por defecto
    
    if filter.SortBy != "" {
        switch filter.SortBy {
        case "questions":
            orderClause = "tests.created_at"
        case "test_title":
            orderClause = "tests.title"
        case "test_level":
            orderClause = "tests.level"
        case "test_created_at":
            orderClause = "tests.created_at"
        case "test_updated_at":
            orderClause = "tests.updated_at"            
        default:
            orderClause = "tests.created_at"
        }
        
        if filter.SortOrder == "asc" {
            orderClause += " ASC"
        } else {
            orderClause += " DESC"
        }
    }

    // Obtener tests con paginación
    var tests []models.Test
    query = query.Order(orderClause)
    
    if TotalFilteredTests > 0 {
        query = query.Offset(offset).Limit(filter.PageSize)
    }
    
    err = query.Find(&tests).Error

    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al obtener tests: " + err.Error()})
        return
    }
   
    // Obtener conteos de preguntas
    var testIDs []uint
    for _, test := range tests {
        testIDs = append(testIDs, test.ID)
    }
    
    var questionCounts []struct {
        TestID uint
        Count  int64
    }
    
    config.DB.Model(&models.Question{}).
        Select("test_id, COUNT(*) as count").
        Where("test_id IN (?)", testIDs).
        Group("test_id").
        Find(&questionCounts)

    questionsMap := make(map[uint]int64)
    for _, qc := range questionCounts {
        questionsMap[qc.TestID] = qc.Count
    }

    // Convertir a TestWithStatusResponse
    testsWithStatus := make([]TestWithStatusResponse, len(tests))
    
    for i, test := range tests {
        testsWithStatus[i] = TestWithStatusResponse{
            Test:           test,
            TotalQuestions: int(questionsMap[test.ID]),
        }
    }

    mainTopics, err := models.GetMainTopics() 
    
    // Crear estadísticas
    stats := NotStartedTestsStats{
        TotalTests:            totalTests,
        TotalFilteredTests: TotalFilteredTests,
        TotalByLevel:          totalByLevel,  // Incluir totales por nivel
    }

    response := NotStartedTestsResponse{
        Tests:         testsWithStatus,
        TotalTests:    totalTests,
        TotalPages:    totalPages,
        CurrentPage:   filter.Page,
        PageSize:      filter.PageSize,
        HasMore:       filter.Page < totalPages,
        MainTopics:    mainTopics,
    }

    c.JSON(http.StatusOK, gin.H{
        "data": response,
        "stats": stats,
    })
}