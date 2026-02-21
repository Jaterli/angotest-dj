package admin

import (
	"net/http"
	"time"
	"fmt"

	"angotest/config"
	"angotest/models"

	"github.com/gin-gonic/gin"
)

// UserQuotaController maneja las operaciones con cuotas de usuario
type UserQuotaController struct{}

// CreateQuotaInput datos para crear/actualizar una cuota
type CreateQuotaInput struct {
	UserID      uint   `json:"user_id" binding:"required"`
	MonthYear   string `json:"month_year" binding:"required,len=7"` // Formato: YYYY-MM
	MaxRequests int    `json:"max_requests" binding:"required,min=1"`
}

// toQuotaResponse convierte un UserQuota a QuotaResponse
func toQuotaResponse(quota *models.UserQuota, user *models.User) *QuotaResponse {
	response := &QuotaResponse{
		ID:           quota.ID,
		UserID:       quota.UserID,
		MonthYear:    quota.MonthYear,
		MaxRequests:  quota.MaxRequests,
		UsedRequests: quota.UsedRequests,
		CreatedAt:    quota.CreatedAt,
		UpdatedAt:    quota.UpdatedAt,
	}

	// Incluir datos del usuario si están disponibles
	if user != nil {
		response.Username = user.Username
		response.UserEmail = user.Email
	}

	return response
}

// UpdateQuotaInput datos para editar una cuota
type UpdateQuotaInput struct {
	MaxRequests *int `json:"max_requests,omitempty" binding:"omitempty,min=1"`
	UsedRequests *int `json:"used_requests,omitempty" binding:"omitempty,min=0"`
}

// GetQuotasFilterInput estructura para los filtros de cuotas
type GetQuotasFilterInput struct {
	Page         int    `form:"page"`
	PageSize     int    `form:"page_size"`
	SortBy       string `form:"sort_by"`
	SortOrder    string `form:"sort_order"`
	Search       string `form:"search"`
	UserID       uint   `form:"user_id"`
	MonthYear    string `form:"month_year"`
	MinRemaining *int   `form:"min_remaining"`
	MaxUsage     *int   `form:"max_usage"`
	MinRequests  *int   `form:"min_requests"`
	MaxRequests  *int   `form:"max_requests"`
	StartDate    string `form:"start_date"`
	EndDate      string `form:"end_date"`
}

// QuotaResponse estructura para la respuesta de cuota (SIN campos calculados)
type QuotaResponse struct {
	ID           uint      `json:"id"`
	UserID       uint      `json:"user_id"`
	Username     string    `json:"username,omitempty"`
	UserEmail    string    `json:"user_email,omitempty"`
	MonthYear    string    `json:"month_year"`
	MaxRequests  int       `json:"max_requests"`
	UsedRequests int       `json:"used_requests"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

// DeleteQuotasInput estructura para recibir los IDs a eliminar
type DeleteQuotasInput struct {
	IDs []uint `json:"ids" binding:"required,min=1"`
}

// GetQuotas maneja la obtención de cuotas con filtros y paginación
func (qc *UserQuotaController) GetAllUserQuotas(c *gin.Context) {
	var input GetQuotasFilterInput
	
	if err := c.ShouldBindQuery(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	// Valores por defecto
	if input.Page == 0 {
		input.Page = 1
	}
	if input.PageSize == 0 {
		input.PageSize = 20
	}
	if input.SortBy == "" {
		input.SortBy = "month_year"
	}
	if input.SortOrder == "" {
		input.SortOrder = "desc"
	}
	
	// Construir consulta base
	db := config.DB.Model(&models.UserQuota{}).
		Preload("User")
	
	// --- OBTENER TOTAL GLOBAL (sin filtros) ---
	var globalTotal int64
	if err := config.DB.Model(&models.UserQuota{}).Count(&globalTotal).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error contando total de cuotas"})
		return
	}
	
	// --- APLICAR FILTROS PARA EL TOTAL FILTRADO ---
	filteredDB := db
	
	// Aplicar búsqueda
	if input.Search != "" {
		search := "%" + input.Search + "%"
		// Búsqueda por username o email del usuario
		filteredDB = filteredDB.Joins("LEFT JOIN users ON users.id = user_quota.user_id").
			Where("users.username LIKE ? OR users.email LIKE ? OR CAST(user_quota.user_id AS TEXT) LIKE ?", 
				search, search, search)
	}
	
	// Filtrar por ID de usuario
	if input.UserID > 0 {
		filteredDB = filteredDB.Where("user_quota.user_id = ?", input.UserID)
	}
	
	// Filtrar por mes/año
	if input.MonthYear != "" {
		filteredDB = filteredDB.Where("user_quota.month_year = ?", input.MonthYear)
	}
	
	// Filtrar por solicitudes mínimas restantes
	if input.MinRemaining != nil {
		// remaining = max_requests - used_requests
		filteredDB = filteredDB.Where("user_quota.max_requests - user_quota.used_requests >= ?", *input.MinRemaining)
	}
	
	// Filtrar por porcentaje de uso máximo
	if input.MaxUsage != nil {
		// Evitar división por cero
		filteredDB = filteredDB.Where("user_quota.max_requests > 0").
			Where("(user_quota.used_requests * 100 / user_quota.max_requests) <= ?", *input.MaxUsage)
	}
	
	// Filtrar por rango de solicitudes máximas
	if input.MinRequests != nil {
		filteredDB = filteredDB.Where("user_quota.max_requests >= ?", *input.MinRequests)
	}
	if input.MaxRequests != nil {
		filteredDB = filteredDB.Where("user_quota.max_requests <= ?", *input.MaxRequests)
	}
	
	// Filtrar por fechas de creación
	if input.StartDate != "" {
		if startDate, err := time.Parse("2006-01-02", input.StartDate); err == nil {
			filteredDB = filteredDB.Where("user_quota.created_at >= ?", startDate)
		}
	}
	
	if input.EndDate != "" {
		if endDate, err := time.Parse("2006-01-02", input.EndDate); err == nil {
			filteredDB = filteredDB.Where("user_quota.created_at <= ?", endDate.Add(24*time.Hour))
		}
	}
	
	// --- OBTENER TOTAL FILTRADO ---
	var filteredTotal int64
	if err := filteredDB.Count(&filteredTotal).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error contando cuotas filtradas"})
		return
	}
	
	// --- APLICAR ORDENAMIENTO Y PAGINACIÓN PARA DATOS FILTRADOS ---
	
	// Manejar ordenamiento especial para campos relacionados
	orderClause := ""
	switch input.SortBy {
	case "user_name":
		// Ordenar por nombre de usuario
		orderClause = "users.username"
		filteredDB = filteredDB.Joins("LEFT JOIN users ON users.id = user_quota.user_id")
	default:
		// Ordenamiento por campos directos
		orderClause = "user_quota." + input.SortBy
	}
	
	if input.SortOrder != "" {
		orderClause += " " + input.SortOrder
	}
	
	// Obtener cuotas con paginación
	var quotas []models.UserQuota
	offset := (input.Page - 1) * input.PageSize
	
	if err := filteredDB.
		Order(orderClause).
		Limit(input.PageSize).
		Offset(offset).
		Find(&quotas).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error obteniendo cuotas"})
		return
	}
	
	// Convertir a respuesta (SIN campos calculados)
	responses := make([]QuotaResponse, len(quotas))
	
	for i, quota := range quotas {
		response := QuotaResponse{
			ID:           quota.ID,
			UserID:       quota.UserID,
			MonthYear:    quota.MonthYear,
			MaxRequests:  quota.MaxRequests,
			UsedRequests: quota.UsedRequests,
			CreatedAt:    quota.CreatedAt,
			UpdatedAt:    quota.UpdatedAt,
		}
		
		// Incluir datos del usuario si están disponibles
		if quota.User.ID != 0 {
			response.Username = quota.User.Username
			response.UserEmail = quota.User.Email
		}
		
		responses[i] = response
	}
	
	// Filtros disponibles para el frontend
	availableFilters := gin.H{
		"total_quotas":        globalTotal,
		"filtered_quotas":     filteredTotal,
		"available_months":    qc.getAvailableMonths(),
		"available_statuses":  []string{"normal", "warning", "critical", "exceeded"},
		"default_max_requests": 5,
	}
	
	// Respuesta con el mismo formato que el endpoint de invitaciones
	c.JSON(http.StatusOK, gin.H{
		"quotas": responses,
		"pagination": gin.H{
			"page":         input.Page,
			"page_size":    input.PageSize,
			"total_items":  filteredTotal,
			"total_pages":  (int(filteredTotal) + input.PageSize - 1) / input.PageSize,
		},
		"filters_applied": input,
		"available_filters": availableFilters,
	})
}

// GetUserQuota obtiene la cuota de un usuario específico
func (qc *UserQuotaController)GetUserQuota(c *gin.Context) {
	userID := c.Param("user_id")
	monthYear := c.Query("month_year")
	
	var quota models.UserQuota
	db := config.DB.Where("user_id = ?", userID)
	
	if monthYear != "" {
		db = db.Where("month_year = ?", monthYear)
	} else {
		db = db.Order("month_year DESC")
	}
	
	if err := db.Preload("User").First(&quota).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "cuota no encontrada"})
		return
	}
	
	// Respuesta SIN campos calculados
	response := QuotaResponse{
		ID:           quota.ID,
		UserID:       quota.UserID,
		MonthYear:    quota.MonthYear,
		MaxRequests:  quota.MaxRequests,
		UsedRequests: quota.UsedRequests,
		CreatedAt:    quota.CreatedAt,
		UpdatedAt:    quota.UpdatedAt,
	}
	
	if quota.User.ID != 0 {
		response.Username = quota.User.Username
		response.UserEmail = quota.User.Email
	}
	
	c.JSON(http.StatusOK, gin.H{
		"quota": response,
	})
}

// GetQuotaStats obtiene estadísticas globales de cuotas
func (qc *UserQuotaController) GetQuotaStats(c *gin.Context) {
	var stats struct {
		TotalUsersWithQuota int64 `json:"total_users_with_quota"`
		TotalRequestsAllowed int64 `json:"total_requests_allowed"`
		TotalRequestsUsed    int64 `json:"total_requests_used"`
		UsersExceedingQuota  int64 `json:"users_exceeding_quota"`
		UsersCritical        int64 `json:"users_critical"`
		UsersWarning         int64 `json:"users_warning"`
	}
	
	currentMonth := time.Now().Format("2006-01")
	
	// Total de usuarios con cuota
	config.DB.Model(&models.UserQuota{}).Distinct("user_id").Count(&stats.TotalUsersWithQuota)
	
	// Total de solicitudes permitidas
	config.DB.Model(&models.UserQuota{}).Select("COALESCE(SUM(max_requests), 0)").Scan(&stats.TotalRequestsAllowed)
	
	// Total de solicitudes usadas
	config.DB.Model(&models.UserQuota{}).Select("COALESCE(SUM(used_requests), 0)").Scan(&stats.TotalRequestsUsed)
	
	// Usuarios que han excedido su cuota (used > max)
	config.DB.Model(&models.UserQuota{}).
		Where("used_requests > max_requests").
		Distinct("user_id").
		Count(&stats.UsersExceedingQuota)
	
	// Usuarios en estado crítico (uso >= 80% y <= 100%)
	config.DB.Model(&models.UserQuota{}).
		Where("max_requests > 0").
		Where("(used_requests * 100 / max_requests) >= 80").
		Where("(used_requests * 100 / max_requests) <= 100").
		Distinct("user_id").
		Count(&stats.UsersCritical)
	
	// Usuarios en estado de advertencia (uso >= 50% y < 80%)
	config.DB.Model(&models.UserQuota{}).
		Where("max_requests > 0").
		Where("(used_requests * 100 / max_requests) >= 50").
		Where("(used_requests * 100 / max_requests) < 80").
		Distinct("user_id").
		Count(&stats.UsersWarning)
	
	// Datos del mes actual
	var currentMonthStats struct {
		TotalRequests int64 `json:"total_requests"`
		UsedRequests  int64 `json:"used_requests"`
	}
	
	config.DB.Model(&models.UserQuota{}).
		Where("month_year = ?", currentMonth).
		Select("COALESCE(SUM(max_requests), 0) as total_requests, COALESCE(SUM(used_requests), 0) as used_requests").
		Scan(&currentMonthStats)
	
	c.JSON(http.StatusOK, gin.H{
		"stats": stats,
		"current_month": gin.H{
			"month":          currentMonth,
			"total_requests": currentMonthStats.TotalRequests,
			"used_requests":  currentMonthStats.UsedRequests,
		},
	})
}

// Helper function para obtener los meses disponibles
func (qc *UserQuotaController) getAvailableMonths() []string {
	var months []string
	config.DB.Model(&models.UserQuota{}).
		Distinct("month_year").
		Order("month_year DESC").
		Limit(12).
		Pluck("month_year", &months)
	
	// Si no hay meses, añadir el mes actual
	if len(months) == 0 {
		months = append(months, time.Now().Format("2006-01"))
	}
	
	return months
}

// GetUserQuotaMonths obtiene los meses disponibles para un usuario
func (qc *UserQuotaController) GetUserQuotaMonths(c *gin.Context) {
	userID := c.Param("user_id")
	
	var months []string
	config.DB.Model(&models.UserQuota{}).
		Where("user_id = ?", userID).
		Distinct("month_year").
		Order("month_year DESC").
		Pluck("month_year", &months)
	
	c.JSON(http.StatusOK, gin.H{
		"months": months,
	})
}


// CreateUserQuota crea una nueva cuota para un usuario
func (qc *UserQuotaController) CreateUserQuota(c *gin.Context) {

	var input CreateQuotaInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Verificar que el usuario existe
	var user models.User
	if err := config.DB.First(&user, input.UserID).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "usuario no encontrado"})
		return
	}

	// Verificar si ya existe una cuota para ese usuario y mes
	var existingQuota models.UserQuota
	if err := config.DB.Where("user_id = ? AND month_year = ?", 
		input.UserID, input.MonthYear).First(&existingQuota).Error; err == nil {
		c.JSON(http.StatusConflict, gin.H{
			"error":   "ya existe una cuota para este usuario y mes",
			"existing": toQuotaResponse(&existingQuota, &user),
		})
		return
	}

	// Crear nueva cuota
	quota := models.UserQuota{
		UserID:      input.UserID,
		MonthYear:   input.MonthYear,
		MaxRequests: input.MaxRequests,
		UsedRequests: 0,
	}

	if err := config.DB.Create(&quota).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error creando cuota"})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"quota":   toQuotaResponse(&quota, &user),
		"message": "Cuota creada exitosamente",
	})
}

// UpdateUserQuota edita una cuota existente
func (qc *UserQuotaController) UpdateUserQuota(c *gin.Context) {

	quotaID := c.Param("id")
	if quotaID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "id de cuota requerido"})
		return
	}

	var input UpdateQuotaInput
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Buscar la cuota
	var quota models.UserQuota
	if err := config.DB.First(&quota, quotaID).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "cuota no encontrada"})
		return
	}

	// Actualizar campos
	if input.MaxRequests != nil {
		quota.MaxRequests = *input.MaxRequests
	}
	
	if input.UsedRequests != nil {
		quota.UsedRequests = *input.UsedRequests
	}

	if err := config.DB.Save(&quota).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error actualizando cuota"})
		return
	}

	// Obtener datos del usuario
	var user models.User
	config.DB.First(&user, quota.UserID)

	c.JSON(http.StatusOK, gin.H{
		"quota":   toQuotaResponse(&quota, &user),
		"message": "Cuota actualizada exitosamente",
	})
}

// DeleteUserQuota elimina una cuota
func (qc *UserQuotaController) DeleteUserQuota(c *gin.Context) {

	quotaID := c.Param("id")
	if quotaID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "id de cuota requerido"})
		return
	}

	// Buscar la cuota
	var quota models.UserQuota
	if err := config.DB.First(&quota, quotaID).Error; err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "cuota no encontrada"})
		return
	}

	// Eliminar cuota
	if err := config.DB.Delete(&quota).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error eliminando cuota"})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "Cuota eliminada exitosamente",
		"deleted": gin.H{
			"id":         quota.ID,
			"user_id":    quota.UserID,
			"month_year": quota.MonthYear,
		},
	})
}


// DeleteQuotasBulk elimina múltiples cuotas
func (qc *UserQuotaController) DeleteQuotasBulk(c *gin.Context) {
	var input DeleteQuotasInput
	
	if err := c.ShouldBindJSON(&input); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	
	// Verificar que todas las cuotas existan
	var count int64
	if err := config.DB.Model(&models.UserQuota{}).
		Where("id IN (?)", input.IDs).
		Count(&count).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error verificando cuotas"})
		return
	}
	
	if count != int64(len(input.IDs)) {
		c.JSON(http.StatusNotFound, gin.H{
			"error": "una o más cuotas no existen",
			"found": count,
			"requested": len(input.IDs),
		})
		return
	}
	
	// Eliminar en lote
	result := config.DB.Where("id IN (?)", input.IDs).Delete(&models.UserQuota{})
	if result.Error != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "error eliminando cuotas"})
		return
	}
	
	c.JSON(http.StatusOK, gin.H{
		"message":       "Cuotas eliminadas exitosamente",
		"deleted_count": result.RowsAffected,
		"deleted_ids":   input.IDs,
	})
}


// Helper function para parsear enteros
func parseInt(value string, defaultValue int) int {
	var result int
	_, err := fmt.Sscanf(value, "%d", &result)
	if err != nil {
		return defaultValue
	}
	return result
}

