package user

import (
	"net/http"
	"sync"

	"angotest/services"
	"angotest/types"

	"github.com/gin-gonic/gin"
)

// GetDashboardData - Obtiene solo los datos del usuario para el dashboard
func GetDashboardData(c *gin.Context) {
	userID := getUserIDFromContext(c)
	if userID == 0 {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "no autorizado"})
		return
	}

	dataService := &services.DataService{}
	
	var wg sync.WaitGroup
	var mu sync.Mutex
	
	var (
		personalData    types.PersonalData
		levelData       map[string]types.LevelData
		totalActiveUsers int
		personalErr      error
		levelErr         error
		activeErr        error
	)
	
	wg.Add(3)
	
	// Obtener data personal
	go func() {
		defer wg.Done()
		data, err := dataService.GetPersonalData(userID)
		mu.Lock()
		personalData = data
		personalErr = err
		mu.Unlock()
	}()
	
	// Obtener data de nivel
	go func() {
		defer wg.Done()
		data, err := dataService.GetPersonalLevelData(userID)
		mu.Lock()
		levelData = data
		levelErr = err
		mu.Unlock()
	}()
	
	// Obtener total usuarios activos
	go func() {
		defer wg.Done()
		count, err := dataService.GetActiveUsersCount()
		mu.Lock()
		totalActiveUsers = count
		activeErr = err
		mu.Unlock()
	}()
	
	wg.Wait()
	
	if personalErr != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener estadísticas personales"})
		return
	}
	
	if levelErr != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener estadísticas por nivel"})
		return
	}
	
	if activeErr != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Error al obtener el nº usuarios activos"})
		return
	}
	
	response := types.DashboardStats{
		PersonalData:     personalData,
		LevelData:        levelData,
		TotalActiveUsers: totalActiveUsers,
	}
	
	c.JSON(http.StatusOK, response)
}

func getUserIDFromContext(c *gin.Context) uint {
	userIDIfc, exists := c.Get("user_id")
	if !exists {
		return 0
	}
	userID, ok := userIDIfc.(uint)
	if !ok {
		return 0
	}
	return userID
}