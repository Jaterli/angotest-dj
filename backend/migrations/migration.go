// main.go o migration.go
func migrateDB() {
    config.DB.AutoMigrate(
        &models.User{},
        &models.Test{},
        &models.Question{},
        &models.Answer{},
        &models.Result{},
        &models.AIRequest{},
        &models.UserQuota{},
        &models.SystemConfig{},
    )
    
    // Insertar configuración inicial si no existe
    var configCount int64
    config.DB.Model(&models.SystemConfig{}).Count(&configCount)
    if configCount == 0 {
        initialConfigs := []models.SystemConfig{
            {Key: "ai_requests_per_month", Value: "5", Description: "Número máximo de tests generados por IA por mes para usuarios gratuitos"},
            {Key: "ai_default_language", Value: "es", Description: "Idioma por defecto para tests generados por IA"},
        }
        for _, cfg := range initialConfigs {
            config.DB.Create(&cfg)
        }
    }
}