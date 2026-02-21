package user

import (
	"encoding/json"
	"net/http"
    "strconv"

	"angotest/config"
	"angotest/models"

	"github.com/gin-gonic/gin"
)


// ====== Obtener todas las preguntas de un test (paginadas) ======
type QuestionsResponse struct {
    TestID      uint              `json:"test_id"`
    Total       int               `json:"total"`
    Page        int               `json:"page"`
    PageSize    int               `json:"page_size"`
    Questions   []QuestionWithAnswers `json:"questions"`
    Progress    float64           `json:"progress"`
}

type QuestionWithAnswers struct {
    ID           uint     `json:"id"`
    QuestionText string   `json:"question_text"`
    Answers      []AnswerResponse `json:"answers"`
}

type AnswerResponse struct {
    ID         uint   `json:"id"`
    AnswerText string `json:"answer_text"`
    // NOTA: No incluir IsCorrect aquí
}

func GetTestQuestions(c *gin.Context) {
    testIDStr  := c.Param("test_id")
    
    // Convertir string a uint
    testID64, err := strconv.ParseUint(testIDStr, 10, 32)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "ID de test inválido"})
        return
    }
    testID := uint(testID64)

    page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
    pageSize, _ := strconv.Atoi(c.DefaultQuery("page_size", "1"))
    
    if page < 1 {
        page = 1
    }
    if pageSize < 1 {
        pageSize = 1
    }
    
    userIDIfc, exists := c.Get("user_id")
    if !exists {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "no autorizado"})
        return
    }
    userID, ok := userIDIfc.(uint)
    if !ok {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "tipo de user_id inválido"})
        return
    }
    
    // Verificar si el usuario tiene progreso en este test
    var result models.Result
    hasProgress := config.DB.Where("user_id = ? AND test_id = ?", userID, testID).
        First(&result).Error == nil
    
    // Obtener total de preguntas
    var totalQuestions int64
    config.DB.Model(&models.Question{}).Where("test_id = ?", testID).Count(&totalQuestions)
    
    // Obtener preguntas paginadas SIN respuestas correctas
    var questions []models.Question
    offset := (page - 1) * pageSize
    
    if err := config.DB.Where("test_id = ?", testID).
        Offset(offset).
        Limit(pageSize).
        Find(&questions).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al obtener preguntas"})
        return
    }
    
    // Obtener respuestas para cada pregunta (sin incluir IsCorrect)
    var questionResponses []QuestionWithAnswers
    for _, q := range questions {
        var answers []models.Answer
        config.DB.Select("id, answer_text").Where("question_id = ?", q.ID).Find(&answers)
        
        // Convertir a AnswerResponse
        var answerResponses []AnswerResponse
        for _, a := range answers {
            answerResponses = append(answerResponses, AnswerResponse{
                ID:         a.ID,
                AnswerText: a.AnswerText,
            })
        }
        
        questionResponses = append(questionResponses, QuestionWithAnswers{
            ID:           q.ID,
            QuestionText: q.QuestionText,
            Answers:      answerResponses,
        })
    }
    
    // Obtener progreso si existe
    progress := 0.0
    if hasProgress && result.Answers != "" {
        var savedAnswers map[uint]uint
        json.Unmarshal([]byte(result.Answers), &savedAnswers)
        if totalQuestions > 0 {
            progress = float64(len(savedAnswers)) / float64(totalQuestions) * 100
        }
    }
    
    c.JSON(http.StatusOK, QuestionsResponse{
        TestID:    testID,
        Total:     int(totalQuestions),
        Page:      page,
        PageSize:  pageSize,
        Questions: questionResponses,
        Progress:  progress,
    })
}

// ====== Obtener una pregunta específica ======
func GetSingleQuestion(c *gin.Context) {
    testID := c.Param("test_id")
    questionNumber, _ := strconv.Atoi(c.Param("question_number"))
    
    if questionNumber < 1 {
        c.JSON(http.StatusBadRequest, gin.H{"error": "número de pregunta inválido"})
        return
    }
    
    // Obtener la pregunta específica
    var question models.Question
    if err := config.DB.Where("test_id = ?", testID).
        Offset(questionNumber - 1).
        Limit(1).
        First(&question).Error; err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "pregunta no encontrada"})
        return
    }
    
    // Obtener respuestas (sin IsCorrect)
    var answers []models.Answer
    config.DB.Select("id, answer_text").Where("question_id = ?", question.ID).Find(&answers)
    
    var answerResponses []AnswerResponse
    for _, a := range answers {
        answerResponses = append(answerResponses, AnswerResponse{
            ID:         a.ID,
            AnswerText: a.AnswerText,
        })
    }
    
    // Obtener total de preguntas para el progreso
    var totalQuestions int64
    config.DB.Model(&models.Question{}).Where("test_id = ?", testID).Count(&totalQuestions)
    
    c.JSON(http.StatusOK, gin.H{
        "question": QuestionWithAnswers{
            ID:           question.ID,
            QuestionText: question.QuestionText,
            Answers:      answerResponses,
        },
        "question_number": questionNumber,
        "total_questions": totalQuestions,
        "has_next":        questionNumber < int(totalQuestions),
        "has_previous":    questionNumber > 1,
    })
}

// ====== Obtener la siguiente pregunta sin responder ======
func GetNextUnansweredQuestion(c *gin.Context) {
    testIDStr := c.Param("test_id")
    
    // Convertir testID
    testID64, err := strconv.ParseUint(testIDStr, 10, 32)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "ID de test inválido"})
        return
    }
    testID := uint(testID64)
    
    userIDIfc, exists := c.Get("user_id")
    if !exists {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "no autorizado"})
        return
    }
    userID, ok := userIDIfc.(uint)
    if !ok {
        c.JSON(http.StatusUnauthorized, gin.H{"error": "tipo de user_id inválido"})
        return
    }
    
    // Verificar resultado existente
    var result models.Result
    err = config.DB.Where("user_id = ? AND test_id = ? AND status != 'completed'", userID, testID).
        First(&result).Error
    
    // Decodificar respuestas
    answeredQuestionIDs := make(map[uint]bool)
    if err == nil && result.Answers != "" {
        var savedAnswers map[uint]uint
        if err := json.Unmarshal([]byte(result.Answers), &savedAnswers); err == nil {
            for qID := range savedAnswers {
                answeredQuestionIDs[qID] = true
            }
        }
    }
    
    // Obtener total de preguntas
    var totalQuestions int64
    config.DB.Model(&models.Question{}).Where("test_id = ?", testID).Count(&totalQuestions)
    
    // Si ya respondió todas, devolver un estado especial
    if int64(len(answeredQuestionIDs)) >= totalQuestions {
        c.JSON(http.StatusOK, gin.H{
            "message": "todas_las_preguntas_respondidas",
            "is_completed": true,
            "answered_count": len(answeredQuestionIDs),
            "total_questions": totalQuestions,
            "progress": 100.0,
        })
        return
    }
    
    // Obtener primera pregunta sin responder
    var question models.Question
    query := config.DB.Where("test_id = ?", testID)
    
    // Excluir preguntas ya respondidas
    if len(answeredQuestionIDs) > 0 {
        var answeredIDs []uint
        for qID := range answeredQuestionIDs {
            answeredIDs = append(answeredIDs, qID)
        }
        query = query.Where("id NOT IN ?", answeredIDs)
    }
    
    // Ordenar y obtener la siguiente
    if err := query.Order("id ASC").First(&question).Error; err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "no se encontró pregunta sin responder"})
        return
    }
    
    // Obtener respuestas
    var answers []models.Answer
    config.DB.Select("id, answer_text").Where("question_id = ?", question.ID).Find(&answers)
    
    var answerResponses []AnswerResponse
    for _, a := range answers {
        answerResponses = append(answerResponses, AnswerResponse{
            ID:         a.ID,
            AnswerText: a.AnswerText,
        })
    }
    
    // Calcular número de pregunta
    var questionNumber int64
    config.DB.Model(&models.Question{}).
        Where("test_id = ? AND id <= ?", testID, question.ID).
        Count(&questionNumber)
    
    // Verificar si hay siguiente
    // var nextQuestion models.Question
    // hasNext := config.DB.Where("test_id = ? AND id > ?", testID, question.ID).
    //     Order("id ASC").
    //     First(&nextQuestion).Error == nil
    
       
    c.JSON(http.StatusOK, gin.H{
        "question": QuestionWithAnswers{
            ID:           question.ID,
            QuestionText: question.QuestionText,
            Answers:      answerResponses,
        },
        "question_number": questionNumber,
        "total_questions": totalQuestions,
        "is_completed":    false,
        "answered_count":  len(answeredQuestionIDs),
        "progress":        float64(len(answeredQuestionIDs)) / float64(totalQuestions) * 100,
    })
}