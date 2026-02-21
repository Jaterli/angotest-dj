package admin

import (
    "net/http"
    "strconv"
    "fmt"
    "time"

    "angotest/config"
    "angotest/models"

    "github.com/gin-gonic/gin"
    "gorm.io/gorm"
)

// ====== Crear Test (solo admin) ======
type CreateTestInput struct {
    Title         string                 `json:"title" binding:"required"`
    Description   string                 `json:"description"`
    MainTopic     string                 `json:"main_topic" binding:"required"`
    SubTopic      string                 `json:"sub_topic" binding:"required"`
    SpecificTopic string                 `json:"specific_topic" binding:"required"`
    Level         string                 `json:"level" binding:"required,oneof=Principiante Intermedio Avanzado"`
    IsActive      bool                   `json:"is_active"`
    Questions     []CreateQuestionInput  `json:"questions" binding:"required"`
}

type CreateQuestionInput struct {
    QuestionText string              `json:"question_text" binding:"required"`
    Answers      []CreateAnswerInput `json:"answers" binding:"required"`
}

type CreateAnswerInput struct {
    AnswerText string `json:"answer_text" binding:"required"`
    IsCorrect  bool   `json:"is_correct"`
}

// ====== Actualizar Test (solo admin) ======
type UpdateTestInput struct {
    Title         string                 `json:"title"`
    Description   string                 `json:"description"`
    MainTopic     string                 `json:"main_topic"`
    SubTopic      string                 `json:"sub_topic"`
    SpecificTopic string                 `json:"specific_topic"`
    Level         string                 `json:"level" binding:"omitempty,oneof=Principiante Intermedio Avanzado"`
    IsActive      *bool                  `json:"is_active"`
    Questions     []UpdateQuestionInput  `json:"questions"`
}

type UpdateQuestionInput struct {
    ID           uint                  `json:"id"`
    QuestionText string                `json:"question_text"`
    Answers      []UpdateAnswerInput   `json:"answers"`
}

type UpdateAnswerInput struct {
    ID         uint   `json:"id"`
    AnswerText string `json:"answer_text"`
    IsCorrect  bool   `json:"is_correct"`
}

func CreateTest(c *gin.Context) {
    var input CreateTestInput
    if err := c.ShouldBindJSON(&input); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Validar nivel
    validLevels := models.GetPredefinedLevels()
    if !models.ContainsString(validLevels, input.Level) {
        c.JSON(http.StatusBadRequest, gin.H{
            "error": "Nivel no válido",
            "valid_levels": validLevels,
        })
        return
    }

    // Insertar nuevos temas
    if input.MainTopic != "" && input.SubTopic != "" && input.SpecificTopic != "" {

        mainTopic := input.MainTopic
        subTopic := input.SubTopic
        specificTopic := input.SpecificTopic
              
        err := models.InsertOrUpdateTopic(
            mainTopic,
            subTopic,
            specificTopic,
            false, //is_predefined
        )
        if err != nil {
            // Solo log el error, no fallar la creación del test
            fmt.Printf("Warning: No se pudo guardar nuevo tema: %v\n", err)
        } else {
            // Invalidar cache ya que añadimos un nuevo topic            
            models.InvalidateTopicsCache()
        }
    } else {
        c.JSON(http.StatusBadRequest, gin.H{
            "error": "Faltan temas",
        })
        return
    }

    // Validar que haya al menos una pregunta
    if len(input.Questions) == 0 {
        c.JSON(http.StatusBadRequest, gin.H{
            "error": "El test debe contener al menos una pregunta",
        })
        return
    }

    // Validar cada pregunta
    for i, question := range input.Questions {
        // Validar que la pregunta tenga texto
        if question.QuestionText == "" {
            c.JSON(http.StatusBadRequest, gin.H{
                "error": fmt.Sprintf("La pregunta %d no tiene texto", i+1),
            })
            return
        }

        // Validar que haya al menos 2 respuestas
        if len(question.Answers) < 2 {
            c.JSON(http.StatusBadRequest, gin.H{
                "error": fmt.Sprintf("La pregunta %d debe tener al menos 2 respuestas", i+1),
            })
            return
        }

        // Validar que haya exactamente una respuesta correcta
        correctCount := 0
        for j, answer := range question.Answers {
            if answer.AnswerText == "" {
                c.JSON(http.StatusBadRequest, gin.H{
                    "error": fmt.Sprintf("La respuesta %d de la pregunta %d no tiene texto", j+1, i+1),
                })
                return
            }
            if answer.IsCorrect {
                correctCount++
            }
        }

        if correctCount != 1 {
            c.JSON(http.StatusBadRequest, gin.H{
                "error": fmt.Sprintf("La pregunta %d debe tener exactamente una respuesta correcta (tiene %d)", i+1, correctCount),
            })
            return
        }
    }

    userIDIfc, _ := c.Get("user_id")
    createdBy := userIDIfc.(uint)

    test := models.Test{
        Title:         input.Title,
        Description:   input.Description,
        MainTopic:     input.MainTopic,
        SubTopic:      input.SubTopic,
        SpecificTopic: input.SpecificTopic,
        Level:         input.Level,
        IsActive:      input.IsActive,
        CreatedBy:     createdBy,
        UpdatedAt:     time.Now(),
    }

    // Crear preguntas y respuestas
    for _, q := range input.Questions {
        question := models.Question{QuestionText: q.QuestionText}
        for _, a := range q.Answers {
            question.Answers = append(question.Answers, models.Answer{
                AnswerText: a.AnswerText,
                IsCorrect:  a.IsCorrect,
            })
        }
        test.Questions = append(test.Questions, question)
    }

    if err := config.DB.Create(&test).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al crear test: " + err.Error()})
        return
    }

    // Invalidar cache de temas después de crear un nuevo test
    models.InvalidateTopicsCache()

    c.JSON(http.StatusCreated, gin.H{
        "test": test,
        "message": "Test creado exitosamente",
        "topics_cache_invalidated": true,
    })
}

func UpdateTest(c *gin.Context) {
    idStr := c.Param("test_id")
    id, err := strconv.ParseUint(idStr, 10, 32)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "ID inválido"})
        return
    }

    // Verificar si el test existe
    var existingTest models.Test
    if err := config.DB.Preload("Questions.Answers").First(&existingTest, id).Error; err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "test no encontrado"})
        return
    }

    var input UpdateTestInput
    if err := c.ShouldBindJSON(&input); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Validar nivel si se proporciona
    if input.Level != "" {
        validLevels := models.GetPredefinedLevels()
        if !models.ContainsString(validLevels, input.Level) {
            c.JSON(http.StatusBadRequest, gin.H{
                "error": "Nivel no válido",
                "valid_levels": validLevels,
            })
            return
        }
    }

    // Actualizar o insertar nuevos temas
    if input.MainTopic != "" || input.SubTopic != "" || input.SpecificTopic != "" {

        mainTopic := input.MainTopic
        subTopic := input.SubTopic
        specificTopic := input.SpecificTopic
        
        // Si no se proporciona algún nivel, usar el existente
        if mainTopic == "" {
            mainTopic = existingTest.MainTopic
        }
        if subTopic == "" {
            subTopic = existingTest.SubTopic
        }
        if specificTopic == "" {
            specificTopic = existingTest.SpecificTopic
        }
        
        err := models.InsertOrUpdateTopic(
            mainTopic,
            subTopic,
            specificTopic,
            false, // is_predefined
        )
        if err != nil {
            // Solo log el error, no fallar la creación del test
            fmt.Printf("Warning: No se pudo guardar nuevo tema: %v\n", err)
        } else {
            // Invalidar cache ya que añadimos un nuevo topic            
            models.InvalidateTopicsCache()
        }

    }

    // Validar preguntas si se proporcionan
    if input.Questions != nil {
        for i, question := range input.Questions {
            // Validar que la pregunta tenga texto si se actualiza
            if question.QuestionText == "" && question.ID == 0 {
                c.JSON(http.StatusBadRequest, gin.H{
                    "error": fmt.Sprintf("La nueva pregunta %d no tiene texto", i+1),
                })
                return
            }

            // Validar respuestas si se proporcionan
            if question.Answers != nil {
                // Para preguntas nuevas, validar que haya al menos 2 respuestas
                if question.ID == 0 && len(question.Answers) < 2 {
                    c.JSON(http.StatusBadRequest, gin.H{
                        "error": fmt.Sprintf("La nueva pregunta %d debe tener al menos 2 respuestas", i+1),
                    })
                    return
                }

                // Validar que haya exactamente una respuesta correcta
                correctCount := 0
                for j, answer := range question.Answers {
                    if answer.AnswerText == "" && answer.ID == 0 {
                        c.JSON(http.StatusBadRequest, gin.H{
                            "error": fmt.Sprintf("La nueva respuesta %d de la pregunta %d no tiene texto", j+1, i+1),
                        })
                        return
                    }
                    if answer.IsCorrect {
                        correctCount++
                    }
                }

                if correctCount != 1 {
                    c.JSON(http.StatusBadRequest, gin.H{
                        "error": fmt.Sprintf("La pregunta %d debe tener exactamente una respuesta correcta (tiene %d)", i+1, correctCount),
                    })
                    return
                }
            }
        }
    }

    // Iniciar transacción
    err = config.DB.Transaction(func(tx *gorm.DB) error {
        // Actualizar información básica del test
        if input.Title != "" {
            existingTest.Title = input.Title
        }
        if input.Description != "" {
            existingTest.Description = input.Description
        }
        if input.MainTopic != "" {
            existingTest.MainTopic = input.MainTopic
        }
        if input.SubTopic != "" {
            existingTest.SubTopic = input.SubTopic
        }
        if input.SpecificTopic != "" {
            existingTest.SpecificTopic = input.SpecificTopic
        }
        if input.Level != "" {
            existingTest.Level = input.Level
        }
        if input.IsActive != nil {
            existingTest.IsActive = *input.IsActive
        }

        existingTest.UpdatedAt = time.Now()

        // Guardar cambios del test
        if err := tx.Save(&existingTest).Error; err != nil {
            return err
        }

        // Procesar preguntas
        if input.Questions != nil {
            // Obtener IDs de preguntas existentes
            var existingQuestionIDs []uint
            for _, q := range existingTest.Questions {
                existingQuestionIDs = append(existingQuestionIDs, q.ID)
            }

            // Procesar cada pregunta del input
            for _, qInput := range input.Questions {
                if qInput.ID == 0 {
                    // Nueva pregunta
                    question := models.Question{
                        TestID:       existingTest.ID,
                        QuestionText: qInput.QuestionText,
                    }
                    
                    // Crear respuestas
                    for _, aInput := range qInput.Answers {
                        question.Answers = append(question.Answers, models.Answer{
                            AnswerText: aInput.AnswerText,
                            IsCorrect:  aInput.IsCorrect,
                        })
                    }
                    
                    if err := tx.Create(&question).Error; err != nil {
                        return err
                    }
                } else {
                    // Pregunta existente - actualizar
                    var question models.Question
                    if err := tx.First(&question, qInput.ID).Error; err != nil {
                        continue // Pregunta no encontrada, saltar
                    }
                    
                    // Actualizar texto de pregunta
                    if qInput.QuestionText != "" {
                        question.QuestionText = qInput.QuestionText
                        if err := tx.Save(&question).Error; err != nil {
                            return err
                        }
                    }
                    
                    // Procesar respuestas
                    if qInput.Answers != nil {
                        // Obtener IDs de respuestas existentes
                        var existingAnswerIDs []uint
                        for _, a := range question.Answers {
                            existingAnswerIDs = append(existingAnswerIDs, a.ID)
                        }
                        
                        // Procesar cada respuesta
                        for _, aInput := range qInput.Answers {
                            if aInput.ID == 0 {
                                // Nueva respuesta
                                answer := models.Answer{
                                    QuestionID: question.ID,
                                    AnswerText: aInput.AnswerText,
                                    IsCorrect:  aInput.IsCorrect,
                                }
                                if err := tx.Create(&answer).Error; err != nil {
                                    return err
                                }
                            } else {
                                // Respuesta existente - actualizar
                                var answer models.Answer
                                if err := tx.First(&answer, aInput.ID).Error; err != nil {
                                    continue // Respuesta no encontrada, saltar
                                }
                                
                                if aInput.AnswerText != "" {
                                    answer.AnswerText = aInput.AnswerText
                                }
                                answer.IsCorrect = aInput.IsCorrect
                                
                                if err := tx.Save(&answer).Error; err != nil {
                                    return err
                                }
                            }
                        }
                        
                        // Eliminar respuestas que no están en el input
                        for _, answerID := range existingAnswerIDs {
                            found := false
                            for _, aInput := range qInput.Answers {
                                if aInput.ID == answerID {
                                    found = true
                                    break
                                }
                            }
                            
                            if !found {
                                if err := tx.Delete(&models.Answer{}, answerID).Error; err != nil {
                                    return err
                                }
                            }
                        }
                    }
                    
                    // Eliminar pregunta de la lista de IDs existentes
                    for i, id := range existingQuestionIDs {
                        if id == qInput.ID {
                            existingQuestionIDs = append(existingQuestionIDs[:i], existingQuestionIDs[i+1:]...)
                            break
                        }
                    }
                }
            }
            
            // Eliminar preguntas que no están en el input
            for _, questionID := range existingQuestionIDs {
                // Primero eliminar respuestas asociadas
                if err := tx.Where("question_id = ?", questionID).Delete(&models.Answer{}).Error; err != nil {
                    return err
                }
                
                // Luego eliminar la pregunta
                if err := tx.Delete(&models.Question{}, questionID).Error; err != nil {
                    return err
                }
            }
        }
        
        return nil
    })
    
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al actualizar test: " + err.Error()})
        return
    }

    // Eliminar topics huérfanos si los hubiera
    rowsAffected, err := models.DeleteOrphanedTopics()
    if err != nil {
        fmt.Printf("Warning: No se pudieron eliminar los topics huérfamos: %v\n", err)
    } else {
        fmt.Printf("Se eliminaron %v topics huérfanos\n", rowsAffected)            
    }  

    // Invalidar cache de temas después de actualizar
    models.InvalidateTopicsCache()
    
    // Obtener el test actualizado
    var updatedTest models.Test
    if err := config.DB.Preload("Questions.Answers").First(&updatedTest, id).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al obtener test actualizado"})
        return
    }
    
    c.JSON(http.StatusOK, gin.H{
        "test": updatedTest, 
        "message": "Test actualizado correctamente",
        "topics_cache_invalidated": true,
    })
}

func DeleteTest(c *gin.Context) {
    idStr := c.Param("test_id")
    id, err := strconv.ParseUint(idStr, 10, 32)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "ID inválido"})
        return
    }

    // Verificar si el test existe
    var test models.Test
    if err := config.DB.First(&test, id).Error; err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "test no encontrado"})
        return
    }

    // Iniciar transacción para eliminar en cascada
    err = config.DB.Transaction(func(tx *gorm.DB) error {
        // 1. Eliminar resultados asociados al test
        if err := tx.Where("test_id = ?", id).Delete(&models.Result{}).Error; err != nil {
            return err
        }

        // 2. Obtener preguntas del test
        var questions []models.Question
        if err := tx.Where("test_id = ?", id).Find(&questions).Error; err != nil {
            return err
        }

        // 3. Eliminar respuestas de cada pregunta
        for _, question := range questions {
            if err := tx.Where("question_id = ?", question.ID).Delete(&models.Answer{}).Error; err != nil {
                return err
            }
        }

        // 4. Eliminar preguntas
        if err := tx.Where("test_id = ?", id).Delete(&models.Question{}).Error; err != nil {
            return err
        }

        // 5. Eliminar invitaciones
        if err := tx.Where("test_id = ?", id).Delete(&models.TestInvitation{}).Error; err != nil {
            return err
        }

        // 6. Finalmente eliminar el test
        if err := tx.Delete(&test).Error; err != nil {
            return err
        }

        return nil
    })

    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al eliminar test: " + err.Error()})
        return
    }

    // Eliminar topics huérfanos si los hubiera
    rowsAffected, err := models.DeleteOrphanedTopics()
    if err != nil {
        fmt.Printf("Warning: No se pudieron eliminar los topics huérfamos: %v\n", err)
    } else {
        fmt.Printf("Se eliminaron %v topics huérfanos\n", rowsAffected)            
    }

    // Invalidar cache de temas después de eliminar
    models.InvalidateTopicsCache()

    c.JSON(http.StatusOK, gin.H{
        "message": "Test eliminado correctamente",
        "topics_cache_invalidated": true,
    })
}


// ====== Obtener todos los tests con paginación, filtrado y ordenación ======

type TestWithCount struct {
    models.Test
    QuestionCount int `json:"question_count"`
}

type AdminTestListResponse struct {
	Tests []TestWithCount  `json:"tests"`
	FiltersApplied   gin.H `json:"filters_applied,omitempty"`
	AvailableFilters gin.H `json:"available_filters,omitempty"`
    Stats            gin.H `json:"stats,omitempty"`  
}

type TestFilter struct {
    Page       int    `form:"page" binding:"omitempty,min=1"`
    PageSize   int    `form:"page_size" binding:"omitempty,min=1,max=100"`
    SortBy     string `form:"sort_by" binding:"omitempty,oneof=id title main_topic sub_topic level is_active updated_at created_at created_by"`
    SortOrder  string `form:"sort_order" binding:"omitempty,oneof=asc desc"`
    MainTopic  string `form:"main_topic" binding:"omitempty"`
    SubTopic   string `form:"sub_topic" binding:"omitempty"`
    Level      string `form:"level" binding:"omitempty,oneof=Principiante Intermedio Avanzado"`
    IsActive   *bool  `form:"is_active" binding:"omitempty"`
    Search     string `form:"search" binding:"omitempty"`
}

func GetAllTests(c *gin.Context) {
    var filter TestFilter
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
    if filter.SortBy == "" {
        filter.SortBy = "created_at"
    }
    if filter.SortOrder == "" {
        filter.SortOrder = "desc"
    }

    // Construir consulta base
    query := config.DB.Model(&models.Test{}).
        Select("tests.*, COUNT(questions.id) as question_count").
        Joins("LEFT JOIN questions ON questions.test_id = tests.id").
        Group("tests.id")


    var totalTests int64
    if err := query.Count(&totalTests).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al contar todos los tests: " + err.Error()})
        return
    }

    var subTopics []string 
    // Aplicar filtros
    if filter.MainTopic != "" {
        query = query.Where("tests.main_topic = ?", filter.MainTopic)
        // Obtener subtemas para el filtro seleccionado
        var err error
        subTopics, err = models.GetSubTopics(filter.MainTopic)
        if err != nil {
            // Manejar error si es necesario, pero no detener la ejecución
            subTopics = []string{}
        }
    }
    if filter.SubTopic != "" {
        query = query.Where("tests.sub_topic = ?", filter.SubTopic)
    }
    if filter.Level != "" {
        query = query.Where("tests.level = ?", filter.Level)
    }
    if filter.IsActive != nil {
        query = query.Where("tests.is_active = ?", *filter.IsActive)
    }
    if filter.Search != "" {
        searchPattern := "%" + filter.Search + "%"
        query = query.Where("tests.title ILIKE ? OR tests.description ILIKE ?", searchPattern, searchPattern)
    }

    // Contar total (con filtros y sin paginación)
    var totalFilteredTests int64
    if err := query.Count(&totalFilteredTests).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al contar los tests filtrados: " + err.Error()})
        return
    }

    // Calcular paginación
    offset := (filter.Page - 1) * filter.PageSize

    // Aplicar ordenación
    sortClause := fmt.Sprintf("%s %s", filter.SortBy, filter.SortOrder)
    query = query.Order(sortClause)

    // Aplicar paginación
    query = query.Offset(offset).Limit(filter.PageSize)

    // Ejecutar consulta
    var tests []TestWithCount
    if err := query.Find(&tests).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "error al obtener tests: " + err.Error()})
        return
    }

	// Obtener filtros disponibles
	mainTopics, _ := models.GetMainTopics()
	levels := models.GetPredefinedLevels()
	statuses := models.GetPredefinedStatus()

	// Construir respuesta estructurada
	response := AdminTestListResponse{
		Tests: tests,
		FiltersApplied: gin.H{
            "page":        filter.Page,
            "page_size":   filter.PageSize,
            "main_topic":  filter.MainTopic,
            "sub_topic":   filter.SubTopic,
            "level":       filter.Level,
            "is_active":   filter.IsActive,
            "search":      filter.Search,
            "sort_by":     filter.SortBy,
            "sort_order":  filter.SortOrder,
		},
		AvailableFilters: gin.H{
			"main_topics": mainTopics,
            "sub_topics":  subTopics, 
			"levels":      levels,
			"statuses":    statuses,
			"roles":       []string{"user", "admin"},
		},
		Stats: gin.H{ 
			"total_tests": totalTests,
			"total_filtered_tests": totalFilteredTests,
		},
	}
	
	c.JSON(http.StatusOK, response)
}

// ====== Obtener test por ID con preguntas y respuestas (admin) ======
func GetTestByID(c *gin.Context) {
	id := c.Param("test_id")

	var test models.Test
	if err := config.DB.Preload("Questions.Answers").First(&test, id).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "test no encontrado"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"test": test})
}
