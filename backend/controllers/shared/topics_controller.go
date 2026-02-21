package shared

import (
    "net/http"
    
    "github.com/gin-gonic/gin"
    "angotest/models"
)


type TopicsController struct{}

// GetTopics obtiene la jerarquía completa de temas
func (tc *TopicsController) GetTopics(c *gin.Context) {
    hierarchy, err := models.GetTopics(false)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    
    c.JSON(http.StatusOK, hierarchy)
}

// GetMainTopics obtiene solo los temas principales
func (tc *TopicsController) GetMainTopics(c *gin.Context) {
    topics, err := models.GetMainTopics()
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    
    c.JSON(http.StatusOK, topics)
}

// GetSubTopics obtiene subtemas de un tema principal
func (tc *TopicsController) GetSubTopics(c *gin.Context) {
    mainTopic := c.Param("main_topic")
    if mainTopic == "" {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Main topic is required"})
        return
    }
    
    subTopics, err := models.GetSubTopics(mainTopic)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    
    c.JSON(http.StatusOK, subTopics)
}

// GetSpecificTopics obtiene temas específicos
func (tc *TopicsController) GetSpecificTopics(c *gin.Context) {
    mainTopic := c.Param("main_topic")
    subTopic := c.Param("sub_topic")

    if mainTopic == "" || subTopic == "" {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Both main_topic and sub_topic are required"})
        return
    }
    
    specificTopics, err := models.GetSpecificTopics(mainTopic, subTopic)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    
    c.JSON(http.StatusOK, specificTopics)
}

// ValidateTopic valida una combinación de temas
func (tc *TopicsController) ValidateTopic(c *gin.Context) {
    var request struct {
        MainTopic     string `json:"main_topic"`
        SubTopic      string `json:"sub_topic"`
        SpecificTopic string `json:"specific_topic"`
    }
    
    if err := c.ShouldBindJSON(&request); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request body"})
        return
    }
    
    isValid, suggestions, err := models.ValidateAndSuggestTopics(
        request.MainTopic, 
        request.SubTopic, 
        request.SpecificTopic,
    )
    
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    
    c.JSON(http.StatusOK, gin.H{
        "valid":      isValid,
        "suggestions": suggestions,
    })
}

// RefreshCache refresca el cache de temas (admin only)
func (tc *TopicsController) RefreshCache(c *gin.Context) {
    models.InvalidateTopicsCache()
    
    _, err := models.GetTopics(true)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to refresh cache"})
        return
    }
    
    c.JSON(http.StatusOK, gin.H{"message": "Topics cache refreshed successfully"})
}

// GetTopicStatistics obtiene estadísticas de temas
func (tc *TopicsController) GetTopicStatistics(c *gin.Context) {
    stats, err := models.GetTopicStatistics()
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    
    c.JSON(http.StatusOK, stats)
}

// GetTopicHierarchy obtiene la estructura jerárquica completa
func (tc *TopicsController) GetTopicHierarchy(c *gin.Context) {
    hierarchy, err := models.GetTopicHierarchy()
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    
    c.JSON(http.StatusOK, hierarchy)
}