package main

import (
	"log"
	"net/http"
	"os"

	"angotest/config"
	"angotest/models"
	"angotest/routes"
	"angotest/controllers/shared"
	"angotest/schedulers"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"	
	"github.com/gin-contrib/cors"
	"time"
)

func main() {

	if os.Getenv("ENV") != "production" {
		if err := godotenv.Load(); err != nil {
			log.Println("⚠️  No se pudo cargar .env file, usando variables del sistema")
		}
	}

	// Comprobación de variables críticas
	requiredVars := []string{"DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME", "JWT_SECRET"}
	for _, envVar := range requiredVars {
		if os.Getenv(envVar) == "" {
			log.Fatalf("❌ Variable de entorno requerida faltante: %s", envVar)
		}
	}

	// // CARGAR VARIABLES DESDE .env
	// if err := godotenv.Load(); err != nil {
	// 	log.Println("⚠️  No se pudo cargar .env file, usando variables del sistema")
	// }

	// // Comprobación de variables críticas
	// requiredVars := []string{"DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME", "JWT_SECRET"}
	// for _, envVar := range requiredVars {
	// 	if os.Getenv(envVar) == "" {
	// 		log.Fatalf("❌ Variable de entorno requerida faltante: %s", envVar)
	// 	}
	// }

	if err := config.ConnectDB(); err != nil {
		log.Fatalf("error conectando a DB: %v", err)
	}
	log.Println("✅ Base de datos inicializada")

	// Inicializar cache de topics
	if err := models.InitTopicsCache(); err != nil {
		log.Printf("Warning: Could not init topics cache: %v", err)
	}	

	// MIGRAR TODOS LOS MODELOS
	if err := config.DB.AutoMigrate(
		&models.User{},		
  		&models.Topic{}, 	
		&models.Test{},
		&models.Question{},
		&models.Answer{},				
		&models.Result{},
 		&models.UserQuota{},		
		&models.SystemConfig{},
  		&models.TestInvitation{},		
        &shared.PasswordResetToken{},		
		//&models.AIRequest{},	
	
	); err != nil {
		log.Fatalf("error en migraciones: %v", err)
	}

	// Arrancar servidor
	r := gin.Default()

	// CORS global
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:4200"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Authorization", "Accept", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	// Para desarrollo local, confiar en localhost y redes privadas
	r.SetTrustedProxies([]string{"127.0.0.1", "::1", "localhost"})

	// Rutas
	routes.SetupRoutes(r)

	// Iniciar schedulers
	schedulerManager := schedulers.NewSchedulerManager()
	schedulerManager.InitSchedulers()
	defer schedulerManager.Stop()


	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("🚀 Servidor iniciado en puerto :%s", port)
	if err := r.Run(":" + port); err != nil && err != http.ErrServerClosed {
		log.Fatalf("❌ Error arrancando servidor: %v", err)
	}
}