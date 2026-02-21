package middleware

import (
	"fmt"
	"net/http"
	"os"
	"strings"

	"angotest/config"
	"angotest/models"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
)


// AuthMiddleware simplificado
func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		tokenStr, err := c.Cookie("auth_token")
		if err != nil {
			authHeader := c.GetHeader("Authorization")
			if authHeader == "" {
				c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "autenticación requerida"})
				return
			}

			parts := strings.SplitN(authHeader, " ", 2)
			if len(parts) != 2 || strings.ToLower(parts[0]) != "bearer" {
				c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "formato Authorization inválido"})
				return
			}
			tokenStr = parts[1]
		}

		secret := os.Getenv("JWT_SECRET")
		if secret == "" {
			c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"error": "configuración inválida"})
			return
		}

		claims := jwt.MapClaims{}
		token, err := jwt.ParseWithClaims(tokenStr, claims, func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("método de firma inesperado: %v", token.Header["alg"])
			}
			return []byte(secret), nil
		})

		if err != nil || !token.Valid {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "token inválido o expirado"})
			return
		}

		userIDFloat, ok := claims["user_id"].(float64)
		if !ok {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "token inválido"})
			return
		}

		userID := uint(userIDFloat)
		var user models.User
		if err := config.DB.First(&user, userID).Error; err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "usuario no encontrado"})
			return
		}

		c.Set("user_id", userID)
		c.Set("user", user)

		if role, ok := claims["role"].(string); ok {
			c.Set("role", role)
		} else {
			c.Set("role", user.Role)
		}

		c.Next()
	}
}


// AdminMiddleware verifica que el usuario sea administrador
func AdminMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Primero obtener el usuario del contexto
		userIfc, exists := c.Get("user")
		if !exists {
			// Si no hay usuario en el contexto, intentar autenticar primero
			// Nota: con cookies, AuthMiddleware ya debería haberse ejecutado
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "autenticación requerida"})
			return
		}

		user, ok := userIfc.(models.User)
		if !ok {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "tipo de usuario inválido"})
			return
		}

		// Verificar que el usuario es administrador
		if user.Role != "admin" {
			c.AbortWithStatusJSON(http.StatusForbidden, gin.H{
				"error": "acceso denegado: se requiere rol de administrador",
				"your_role": user.Role,
			})
			return
		}

		c.Next()
	}
}

// UserMiddleware verifica que el usuario tenga al menos rol de usuario
func UserMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		userIfc, exists := c.Get("user")
		if !exists {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "autenticación requerida"})
			return
		}

		user, ok := userIfc.(models.User)
		if !ok {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "tipo de usuario inválido"})
			return
		}

		// Verificar que el usuario tiene al menos rol de usuario
		if user.Role != "user" && user.Role != "guest" && user.Role != "admin" {
			c.AbortWithStatusJSON(http.StatusForbidden, gin.H{
				"error": "acceso denegado: se requiere rol de usuario",
				"your_role": user.Role,
			})
			return
		}

		c.Next()
	}

}


// OptionalAuthMiddleware obtiene el usuario si está autenticado, pero no falla si no lo está
func OptionalAuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// Intentar obtener token de cookie primero
		tokenStr, err := c.Cookie("auth_token")
		if err != nil {
			// Fallback a header Authorization
			authHeader := c.GetHeader("Authorization")
			if authHeader != "" {
				parts := strings.SplitN(authHeader, " ", 2)
				if len(parts) == 2 && strings.ToLower(parts[0]) == "bearer" {
					tokenStr = parts[1]
				}
			}
		}

		// Si no hay token, continuar sin usuario
		if tokenStr == "" {
			c.Next()
			return
		}

		// Verificar secret
		secret := os.Getenv("JWT_SECRET")
		if secret == "" {
			// Si no hay secret, continuar sin autenticación
			c.Next()
			return
		}

		claims := jwt.MapClaims{}
		token, err := jwt.ParseWithClaims(tokenStr, claims, func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, fmt.Errorf("método de firma inesperado: %v", token.Header["alg"])
			}
			return []byte(secret), nil
		})

		// Si hay error en el token, continuar sin usuario
		if err != nil || !token.Valid {
			c.Next()
			return
		}

		// Extraer claims
		claims, ok := token.Claims.(jwt.MapClaims)
		if !ok {
			c.Next()
			return
		}

		// Obtener user_id
		userIDFloat, ok := claims["user_id"].(float64)
		if !ok {
			c.Next()
			return
		}

		userID := uint(userIDFloat)

		// Buscar usuario en la BD (si falla, continuamos igual)
		var user models.User
		if err := config.DB.First(&user, userID).Error; err == nil {
			// Usuario encontrado, establecer en contexto
			c.Set("user_id", userID)
			c.Set("user", user)
			
			// Establecer rol
			if role, ok := claims["role"].(string); ok {
				c.Set("role", role)
			} else {
				c.Set("role", user.Role)
			}

			// También establecer una bandera de autenticación
			c.Set("is_authenticated", true)
		} else {
			// Usuario no encontrado, pero establecer bandera de autenticado como falso
			c.Set("is_authenticated", false)
		}

		c.Next()
	}
}
