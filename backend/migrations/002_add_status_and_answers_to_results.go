// migrations/002_add_status_and_answers_to_results.go
package main

import (
    "angotest/config"
    "angotest/models"
    "gorm.io/gorm"
)

func main() {
    db := config.DB
    
    // Añadir columnas a la tabla results
    db.AutoMigrate(&models.Result{})
    
    // Establecer valores por defecto para los registros existentes
    db.Model(&models.Result{}).Where("status IS NULL").Update("status", "completed")
    
    // Crear índices compuestos para mejor rendimiento
    db.Exec(`
        CREATE INDEX IF NOT EXISTS idx_user_test_status 
        ON results(user_id, test_id, status);
        
        CREATE INDEX IF NOT EXISTS idx_user_status 
        ON results(user_id, status);
    `)
}