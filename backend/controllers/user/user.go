package user

import (
	"net/http"
    "time"
    "strings"
	"fmt"

	"angotest/config"
	"angotest/models"

	"github.com/gin-gonic/gin"
    "golang.org/x/crypto/bcrypt"
)

type updateProfileInput struct {
	Username  string    `json:"username" binding:"required,min=3,max=30"`
	FirstName string    `json:"first_name" binding:"required"`
	LastName  string    `json:"last_name" binding:"required"`
	Phone     string    `json:"phone"`
	Address   string    `json:"address"`
	Country   string    `json:"country" binding:"required"`
	BirthDate string 	`json:"birth_date" binding:"required"`
}

func UpdateProfile(c *gin.Context) {
	// Obtener el ID del usuario autenticado
	userIDIfc, exists := c.Get("user_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "no autenticado"})
		return
	}
	userID := userIDIfc.(uint)

	var input updateProfileInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Parsear la fecha de string a time.Time
	birthDate, err := time.Parse("2006-01-02", input.BirthDate)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "formato de fecha inválido. Use YYYY-MM-DD"})
		return
	}

	// Validar unicidad del username (excepto para el usuario actual)
	var existingUser models.User
	if err := config.DB.Where("username = ? AND id != ?", input.Username, userID).First(&existingUser).Error; err == nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "el nombre de usuario ya está en uso"})
		return
	}

	var user models.User
	if err := config.DB.First(&user, userID).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "usuario no encontrado"})
		return
	}

	// Actualizar campos permitidos (sin email)
	user.Username = input.Username
	user.FirstName = input.FirstName
	user.LastName = input.LastName
	user.Phone = input.Phone
	user.Address = input.Address
	user.Country = input.Country
	user.BirthDate = birthDate

	if err := config.DB.Save(&user).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error al actualizar usuario"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Usuario actualizado correctamente",
		"user":    models.ToUserResponse(&user),
	})
}

// Estructura para el nuevo endpoint combinado
type updateEmailPasswordInput struct {
	CurrentPassword string `json:"current_password" binding:"required"`
	NewEmail        string `json:"new_email,omitempty" binding:"omitempty,email"`
	NewPassword     string `json:"new_password,omitempty" binding:"omitempty,min=6"`
}

func UpdateEmailPassword(c *gin.Context) {
	userIDIfc, exists := c.Get("user_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "no autenticado"})
		return
	}
	userID := userIDIfc.(uint)

	var input updateEmailPasswordInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Validar que al menos se proporcione email nuevo o contraseña nueva
	if input.NewEmail == "" && input.NewPassword == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "debe proporcionar al menos un nuevo email o una nueva contraseña"})
		return
	}

	var user models.User
	if err := config.DB.First(&user, userID).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "usuario no encontrado"})
		return
	}

	// Verificar contraseña actual
	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(input.CurrentPassword)); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "contraseña actual incorrecta"})
		return
	}

	// Iniciar una transacción para asegurar consistencia
	tx := config.DB.Begin()
	defer func() {
		if r := recover(); r != nil {
			tx.Rollback()
		}
	}()

	// Si se proporciona nuevo email
	if input.NewEmail != "" {
		// Validar que el nuevo email no esté en uso
		var existingUser models.User
		if err := tx.Where("email = ? AND id != ?", strings.ToLower(input.NewEmail), userID).First(&existingUser).Error; err == nil {
			tx.Rollback()
			c.JSON(http.StatusBadRequest, gin.H{"error": "el email ya está en uso"})
			return
		}

		// Actualizar email
		user.Email = strings.ToLower(input.NewEmail)
		
		// Aquí podrías agregar lógica para enviar email de confirmación
		// Por ejemplo, marcar el email como no verificado y enviar un correo de verificación
		// user.EmailVerified = false
		// sendVerificationEmail(user.Email)
	}

	// Si se proporciona nueva contraseña
	if input.NewPassword != "" {
		// Generar nuevo hash para la contraseña
		pwHash, err := bcrypt.GenerateFromPassword([]byte(input.NewPassword), bcrypt.DefaultCost)
		if err != nil {
			tx.Rollback()
			c.JSON(http.StatusInternalServerError, gin.H{"error": "no se pudo procesar la nueva contraseña"})
			return
		}
		user.PasswordHash = string(pwHash)
	}

	if err := tx.Save(&user).Error; err != nil {
		tx.Rollback()
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error al actualizar datos"})
		return
	}

	// Commit de la transacción
	if err := tx.Commit().Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error al guardar cambios"})
		return
	}

	// Construir mensaje de respuesta
	message := ""
	if input.NewEmail != "" && input.NewPassword != "" {
		message = "Email y contraseña actualizados correctamente. Por favor, revisa tu nuevo email para confirmar el cambio."
	} else if input.NewEmail != "" {
		message = "Email actualizado correctamente. Por favor, revisa tu nuevo email para confirmar el cambio."
	} else {
		message = "Contraseña actualizada correctamente."
	}

	c.JSON(http.StatusOK, gin.H{
		"message": message,
		"user":    models.ToUserResponse(&user),
	})
}


// Estructura para completar perfil de guest
type updateGuestProfileInput struct {
	Username        string `json:"username" binding:"required,min=3,max=30"`
	Email           string `json:"email" binding:"required,email"`
	FirstName       string `json:"first_name" binding:"required"`
	LastName        string `json:"last_name" binding:"required"`
	Phone           string `json:"phone"`
	Address         string `json:"address"`
	Country         string `json:"country" binding:"required"`
	BirthDate       string `json:"birth_date" binding:"required"`
	NewPassword     string `json:"new_password" binding:"required,min=6"`
}

func UpdateGuestProfile(c *gin.Context) {
	// Obtener el ID del usuario autenticado
	userIDIfc, exists := c.Get("user_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "no autenticado"})
		return
	}
	userID := userIDIfc.(uint)

	var input updateGuestProfileInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Parsear la fecha de string a time.Time
	birthDate, err := time.Parse("2006-01-02", input.BirthDate)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "formato de fecha inválido. Use YYYY-MM-DD"})
		return
	}

	var user models.User
	if err := config.DB.First(&user, userID).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "usuario no encontrado"})
		return
	}

	// Verificar que el usuario sea guest
	if user.Role != "guest" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "esta función solo está disponible para usuarios guest"})
		return
	}

	// Validar unicidad del username
	var existingUser models.User
	if err := config.DB.Where("username = ? AND id != ?", input.Username, userID).First(&existingUser).Error; err == nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "el nombre de usuario ya está en uso"})
		return
	}

	// Validar unicidad del email
	if err := config.DB.Where("email = ? AND id != ?", strings.ToLower(input.Email), userID).First(&existingUser).Error; err == nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "el email ya está en uso"})
		return
	}

	// Iniciar transacción
	tx := config.DB.Begin()
	defer func() {
		if r := recover(); r != nil {
			tx.Rollback()
		}
	}()

	// Actualizar todos los campos del usuario
	user.Username = input.Username
	user.Email = strings.ToLower(input.Email)
	user.FirstName = input.FirstName
	user.LastName = input.LastName
	user.Phone = input.Phone
	user.Address = input.Address
	user.Country = input.Country
	user.BirthDate = birthDate
	user.Role = "user" // Cambiar rol de guest a user

	// Actualizar contraseña
	pwHash, err := bcrypt.GenerateFromPassword([]byte(input.NewPassword), bcrypt.DefaultCost)
	if err != nil {
		tx.Rollback()
		c.JSON(http.StatusInternalServerError, gin.H{"error": "no se pudo procesar la nueva contraseña"})
		return
	}
	user.PasswordHash = string(pwHash)

	if err := tx.Save(&user).Error; err != nil {
		tx.Rollback()
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error al actualizar usuario"})
		return
	}

	// Commit de la transacción
	if err := tx.Commit().Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error al guardar cambios"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Perfil actualizado correctamente. Ahora eres un usuario permanente.",
		"user":    models.ToUserResponse(&user),
	})
}


// Estructura para confirmación de eliminación de cuenta
type deactivateAccountInput struct {
	CurrentPassword string `json:"current_password" binding:"required"`
	ConfirmText     string `json:"confirm_text" binding:"required,eq=CONFIRMAR ELIMINAR CUENTA"`
}

// DeactivateAccount permite al usuario deactivar su propia cuenta
func DeactivateAccount(c *gin.Context) {
	// Obtener el ID del usuario autenticado
	userIDIfc, exists := c.Get("user_id")
	if !exists {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "no autenticado"})
		return
	}
	userID := userIDIfc.(uint)

	// Verificar que no sea el usuario con ID = 1
	if userID == 1 {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Esta operación no está permitida.",
		})
		return
	}

	var input deactivateAccountInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	var user models.User
	if err := config.DB.First(&user, userID).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "usuario no encontrado"})
		return
	}

	// Verificar contraseña actual
	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(input.CurrentPassword)); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "contraseña actual incorrecta"})
		return
	}

	// Confirmación con texto específico
	if input.ConfirmText != "CONFIRMAR ELIMINAR CUENTA" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "debes escribir 'CONFIRMAR ELIMINAR CUENTA' para confirmar"})
		return
	}

	// Verificar si existe el usuario con ID = 1 para transferencia
	var targetUser models.User
	if err := config.DB.First(&targetUser, 1).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "no se puede completar la eliminación. Consulte con el administrador del sistema para resolver este problema",
		})
		return
	}

	// Verificar que el usuario destino no esté eliminado
	if !targetUser.DeletedAt.Time.IsZero() {
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "no se puede completar la eliminación. Consulte con el administrador del sistema para resolver este problema",
		})
		return
	}

	// Iniciar transacción
	tx := config.DB.Begin()

	// 1. Transferir tests al usuario ID = 1
	//tx.Model(&models.Test{}).Where("created_by = ?", userID).Update("created_by", 1)
	
	// 2. Transferir resultados al usuario ID = 1
	//tx.Model(&models.Result{}).Where("user_id = ?", userID).Update("user_id", 1)
	
	// 3. Eliminar quotas
	tx.Where("user_id = ?", userID).Delete(&models.UserQuota{})
	
	// 4. Eliminar invitaciones
	tx.Where("invited_by = ?", userID).Delete(&models.TestInvitation{})

	// 5. Anonimizar usuario
	user.Username = fmt.Sprintf("del_%s_%d", user.Username, userID)
	emailLocal := strings.Split(user.Email, "@")[0]
	user.Email = fmt.Sprintf("%s_%d@deleted.local", emailLocal, userID)
	user.Role = "deleted"
	user.FirstName = "Deleted"
	user.LastName = "User"
	user.Phone = ""
	user.Address = ""
	user.Country = ""
	user.BirthDate = time.Time{}
	
	tx.Save(&user)
	tx.Delete(&user)

	// Commit
	if err := tx.Commit().Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error al desactivar la cuenta"})
		return
	}

	// Respuesta de éxito
	c.JSON(http.StatusOK, gin.H{
		"message": "Tu cuenta ha sido desactivada correctamente.",
	})
}