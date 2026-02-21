// schedulers/mark_in_progress_as_abandoned.go
package schedulers

import (
	"log"
	"time"
	"strconv"

	"angotest/config"
	"angotest/models"
)

// MarkInProgressAsAbandonedScheduler es la versión para el scheduler (sin Gin)
func MarkInProgressAsAbandonedScheduler() {
	startTime := time.Now()
	
	// Obtener la configuración de días desde system_configs
	var systemConfig models.SystemConfig
	days := 7 // valor por defecto
	
	if err := config.DB.Where("key = ?", "mark_in_progress_as_abandoned_after_days").First(&systemConfig).Error; err == nil {
		if val, err := strconv.Atoi(systemConfig.Value); err == nil {
			days = val
		}
	}
	
	processAbandonedTestsScheduler(days, startTime)
}

// processAbandonedTestsScheduler realiza la actualización de los tests (sin Gin)
func processAbandonedTestsScheduler(days int, startTime time.Time) {
	// Calcular la fecha límite (updated_at debe ser menor a esta fecha)
	thresholdDate := time.Now().AddDate(0, 0, -days)
	
	// Actualizar los resultados que están en in_progress y tienen updated_at anterior a la fecha límite
	result := config.DB.Model(&models.Result{}).
		Where("status = ?", "in_progress").
		Where("updated_at < ?", thresholdDate).
		Update("status", "abandoned")
	
	if result.Error != nil {
		log.Printf("❌ Error al actualizar los tests: %v", result.Error)
		return
	}
	
	executionTime := time.Since(startTime)
	
	if result.RowsAffected > 0 {
		log.Printf("✅ %d tests marcados como abandonados en %v (threshold: %s)", 
			result.RowsAffected, 
			executionTime,
			thresholdDate.Format("2006-01-02 15:04:05"))
	} else {
		log.Printf("ℹ️ No se encontraron tests in_progress anteriores a %s", 
			thresholdDate.Format("2006-01-02"))
	}
}