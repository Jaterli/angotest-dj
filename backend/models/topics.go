package models

import (
    "sort"
    "strings"
    "sync"
    "time"
    "fmt"
    "angotest/config"
)

// Estructuras para la jerarquía de temas
type TopicStructure map[string]SubTopics
type SubTopics map[string][]string


// Estructuras de respuesta para temas
type TopicNode struct {
    Name     string       `json:"name"`
    Children []*TopicNode `json:"children,omitempty"`
}

type TopicSummary struct {
    MainTopic      string   `json:"main_topic"`
    SubTopic       string   `json:"sub_topic"`
    SpecificTopic  string   `json:"specific_topic"`
    TestCount      int      `json:"test_count"`
    LastUpdated    string   `json:"last_updated,omitempty"`
}

type FullTopicStructure struct {
    MainTopic string   `json:"main_topic"`
    SubTopics []string `json:"sub_topics"`
}

type TopicHierarchyResponse struct {
    MainTopics []string           `json:"main_topics"`
    Hierarchy  TopicStructure     `json:"hierarchy,omitempty"`
}

// Variables de cache
var (
    topicsCache     TopicStructure
    topicsMutex     sync.RWMutex
    topicsCacheLoaded bool
    topicsCacheExpiration time.Time
    topicsCacheDuration   = 5 * time.Minute
)

// ==================== FUNCIONES DE BASE DE DATOS ====================

// GetTopicsFromDB obtiene todos los temas de la tabla topics
func GetTopicsFromDB() (TopicStructure, error) {
    if config.DB == nil {
        return make(TopicStructure), nil
    }
    
    var topics []Topic
    
    // Consulta para obtener todos los topics
    err := config.DB.
        //Where("is_predefined = ?", true). // descomentar para obtener solo los predefinidos
        Order("main_topic, sub_topic, specific_topic").
        Find(&topics).Error
    
    if err != nil {
        return nil, err
    }
    
    // Construir la jerarquía
    hierarchy := make(TopicStructure)
    
    for _, topic := range topics {
        // Inicializar mapa de subtemas si no existe
        if _, exists := hierarchy[topic.MainTopic]; !exists {
            hierarchy[topic.MainTopic] = make(map[string][]string)
        }
        
        // Agregar tema específico si no existe
        specificTopics := hierarchy[topic.MainTopic][topic.SubTopic]
        if !ContainsString(specificTopics, topic.SpecificTopic) {
            hierarchy[topic.MainTopic][topic.SubTopic] = append(specificTopics, topic.SpecificTopic)
        }
    }
    
    // Ordenar cada nivel alfabéticamente
    for mainTopic, subTopics := range hierarchy {
        for subTopic, specificTopics := range subTopics {
            sort.Strings(specificTopics)
            hierarchy[mainTopic][subTopic] = specificTopics
        }
    }
    
    return hierarchy, nil
}

// GetTopicsFromDBWithCount obtiene temas con conteo de tests asociados
func GetTopicsFromDBWithCount() ([]TopicSummary, error) {
    if config.DB == nil {
        return []TopicSummary{}, nil
    }
    
    var summaries []TopicSummary
    
    // Subconsulta para contar tests por tema
    err := config.DB.Table("topics t").
        Select(`
            t.main_topic,
            t.sub_topic, 
            t.specific_topic,
            COUNT(DISTINCT ts.id) as test_count,
            MAX(ts.updated_at) as last_updated
        `).
        Joins("LEFT JOIN tests ts ON t.main_topic = ts.main_topic AND t.sub_topic = ts.sub_topic AND t.specific_topic = ts.specific_topic").
        Group("t.main_topic, t.sub_topic, t.specific_topic").
        Order("t.main_topic, t.sub_topic, t.specific_topic").
        Scan(&summaries).Error
    
    if err != nil {
        return nil, err
    }
    
    return summaries, nil
}

// InsertOrUpdateTopic inserta o actualiza un topic
func InsertOrUpdateTopic(mainTopic, subTopic, specificTopic string, isPredefined bool) error {
    if config.DB == nil {
        return nil
    }
    
    var topic Topic
    result := config.DB.Where("main_topic = ? AND sub_topic = ? AND specific_topic = ?", 
        mainTopic, subTopic, specificTopic).First(&topic)
    
    if result.Error != nil && result.Error.Error() != "record not found" {
        return result.Error
    }
    
    if result.RowsAffected == 0 {
        // Insertar nuevo
        topic = Topic{
            MainTopic:     mainTopic,
            SubTopic:      subTopic,
            SpecificTopic: specificTopic,
            IsPredefined:  isPredefined,
        }
        fmt.Printf("Se añadieron nuevos topics.\n")            
        return config.DB.Create(&topic).Error    
    }

    return nil
}

// BulkInsertTopics inserta múltiples topics en una transacción
func BulkInsertTopics(topics []Topic) error {
    if config.DB == nil || len(topics) == 0 {
        return nil
    }
    
    tx := config.DB.Begin()
    defer func() {
        if r := recover(); r != nil {
            tx.Rollback()
        }
    }()
    
    for _, topic := range topics {
        // Usar cláusula ON DUPLICATE KEY UPDATE o similar
        // En GORM podemos usar FirstOrCreate
        var existing Topic
        err := tx.Where("main_topic = ? AND sub_topic = ? AND specific_topic = ?",
            topic.MainTopic, topic.SubTopic, topic.SpecificTopic).
            First(&existing).Error
        
        if err != nil && err.Error() == "record not found" {
            if err := tx.Create(&topic).Error; err != nil {
                tx.Rollback()
                return err
            }
        } else if err == nil {
            // Actualizar si existe
            existing.IsPredefined = topic.IsPredefined
            if err := tx.Save(&existing).Error; err != nil {
                tx.Rollback()
                return err
            }
        } else {
            tx.Rollback()
            return err
        }
    }
    
    return tx.Commit().Error
}


// ==================== FUNCIONES DE CACHE ====================

// GetTopics obtiene temas con cache
func GetTopics(forceRefresh bool) (TopicStructure, error) {
    topicsMutex.RLock()
    if !forceRefresh && topicsCacheLoaded && time.Now().Before(topicsCacheExpiration) {
        defer topicsMutex.RUnlock()
        return topicsCache, nil
    }
    topicsMutex.RUnlock()
    
    // Refrescar cache
    topicsMutex.Lock()
    defer topicsMutex.Unlock()
    
    hierarchy, err := GetTopicsFromDB()
    if err != nil {
        // Si hay error, mantener cache anterior si existe
        if topicsCacheLoaded {
            return topicsCache, err
        }
        return make(TopicStructure), err
    }
    
    // Actualizar cache
    topicsCache = hierarchy
    topicsCacheLoaded = true
    topicsCacheExpiration = time.Now().Add(topicsCacheDuration)
    
    return hierarchy, nil
}

// InitTopicsCache inicializa el cache de temas
func InitTopicsCache() error {
    _, err := GetTopics(true)
    return err
}

// InvalidateTopicsCache invalida el cache de temas
func InvalidateTopicsCache() {
    topicsMutex.Lock()
    defer topicsMutex.Unlock()
    
    topicsCacheLoaded = false
    topicsCache = nil
}

// ==================== FUNCIONES PÚBLICAS ====================

// GetMainTopics obtiene todos los temas principales
func GetMainTopics() ([]string, error) {
    hierarchy, err := GetTopics(false)
    if err != nil {
        return nil, err
    }
    
    topics := make([]string, 0, len(hierarchy))
    for topic := range hierarchy {
        topics = append(topics, topic)
    }
    sort.Strings(topics)
    return topics, nil
}

// GetSubTopics obtiene subtemas para un tema principal
func GetSubTopics(mainTopic string) ([]string, error) {
    hierarchy, err := GetTopics(false)
    if err != nil {
        return nil, err
    }
    
    if subTopicsMap, exists := hierarchy[mainTopic]; exists {
        subTopics := make([]string, 0, len(subTopicsMap))
        for subTopic := range subTopicsMap {
            subTopics = append(subTopics, subTopic)
        }
        sort.Strings(subTopics)
        return subTopics, nil
    }
    return []string{}, nil
}

// GetSpecificTopics obtiene temas específicos para un tema principal y subtema
func GetSpecificTopics(mainTopic, subTopic string) ([]string, error) {
    hierarchy, err := GetTopics(false)
    if err != nil {
        return nil, err
    }
    
    if subTopicsMap, exists := hierarchy[mainTopic]; exists {
        if specificTopics, exists := subTopicsMap[subTopic]; exists {
            topics := make([]string, len(specificTopics))
            copy(topics, specificTopics)
            sort.Strings(topics)
            return topics, nil
        }
    }
    return []string{}, nil
}

// ValidateTopicHierarchy valida si la combinación de temas existe
func ValidateTopicHierarchy(mainTopic, subTopic, specificTopic string) (bool, error) {
    hierarchy, err := GetTopics(false)
    if err != nil {
        return false, err
    }
    
    if subTopicsMap, exists := hierarchy[mainTopic]; exists {
        if specificTopics, exists := subTopicsMap[subTopic]; exists {
            for _, topic := range specificTopics {
                if topic == specificTopic {
                    return true, nil
                }
            }
        }
    }
    return false, nil
}

// GetTopicStatistics obtiene estadísticas de temas
func GetTopicStatistics() ([]TopicSummary, error) {
    return GetTopicsFromDBWithCount()
}

// GetTopicTree obtiene la estructura completa en forma de árbol
func GetTopicTree() ([]TopicNode, error) {
    hierarchy, err := GetTopics(false)
    if err != nil {
        return nil, err
    }
    
    var tree []TopicNode
    
    for mainTopic, subTopics := range hierarchy {
        mainNode := TopicNode{Name: mainTopic}
        
        for subTopic, specificTopics := range subTopics {
            subNode := TopicNode{Name: subTopic}
            
            for _, specificTopic := range specificTopics {
                subNode.Children = append(subNode.Children, &TopicNode{
                    Name: specificTopic,
                })
            }
            
            mainNode.Children = append(mainNode.Children, &subNode)
        }
        
        tree = append(tree, mainNode)
    }
    
    // Ordenar árbol
    sort.Slice(tree, func(i, j int) bool {
        return tree[i].Name < tree[j].Name
    })
    
    for i := range tree {
        sort.Slice(tree[i].Children, func(j, k int) bool {
            return tree[i].Children[j].Name < tree[i].Children[k].Name
        })
    }
    
    return tree, nil
}

// ValidateAndSuggestTopics valida y sugiere temas similares
func ValidateAndSuggestTopics(mainTopic, subTopic, specificTopic string) (bool, []string, error) {
    hierarchy, err := GetTopics(false)
    if err != nil {
        return false, nil, err
    }
    
    // Validación exacta
    if subTopicsMap, exists := hierarchy[mainTopic]; exists {
        if specificTopics, exists := subTopicsMap[subTopic]; exists {
            for _, topic := range specificTopics {
                if topic == specificTopic {
                    return true, nil, nil
                }
            }
        }
    }
    
    // Si no existe, buscar sugerencias
    var suggestions []string
    
    if subTopicsMap, exists := hierarchy[mainTopic]; exists {
        if specificTopics, exists := subTopicsMap[subTopic]; exists {
            // Buscar temas específicos similares
            for _, topic := range specificTopics {
                if len(suggestions) < 3 && containsStringFuzzy(topic, specificTopic) {
                    suggestions = append(suggestions, topic)
                }
            }
        } else {
            // Sugerir subtemas para este tema principal
            for st := range subTopicsMap {
                if len(suggestions) < 3 && containsStringFuzzy(st, subTopic) {
                    suggestions = append(suggestions, st)
                }
            }
        }
    }
    
    return false, suggestions, nil
}

// ==================== FUNCIONES PRIVADAS ====================

// containsStringFuzzy función helper para búsqueda fuzzy
func containsStringFuzzy(str, substr string) bool {
    str = strings.ToLower(str)
    substr = strings.ToLower(substr)
    return strings.Contains(str, substr) || strings.Contains(substr, str)
}

// GetTopicHierarchy obtiene la jerarquía completa
func GetTopicHierarchy() (TopicHierarchyResponse, error) {
    hierarchy, err := GetTopics(false)
    if err != nil {
        return TopicHierarchyResponse{}, err
    }
    
    mainTopics := make([]string, 0, len(hierarchy))
    for topic := range hierarchy {
        mainTopics = append(mainTopics, topic)
    }
    sort.Strings(mainTopics)
    
    return TopicHierarchyResponse{
        MainTopics: mainTopics,
        Hierarchy:  hierarchy,
    }, nil
}

// GetAllTopics obtiene todos los topics (para administración)
func GetAllTopics() ([]Topic, error) {
    if config.DB == nil {
        return []Topic{}, nil
    }
    
    var topics []Topic
    err := config.DB.Order("main_topic, sub_topic, specific_topic").Find(&topics).Error
    if err != nil {
        return nil, err
    }
    return topics, nil
}


// DeleteOrphanedTopics elimina topics que no están referenciados en tests y no son predefinidos
func DeleteOrphanedTopics() (int64, error) {
    if config.DB == nil {
        return 0, nil
    }

    // Consulta para encontrar topics que pueden ser eliminados
    // 1. No deben estar referenciados en ningún test
    // 2. is_predefined debe ser false
    result := config.DB.
        Where("is_predefined = ?", false).
        Where("NOT EXISTS (SELECT 1 FROM tests t WHERE t.main_topic = topics.main_topic AND t.sub_topic = topics.sub_topic AND t.specific_topic = topics.specific_topic)").
        Delete(&Topic{})

    if result.Error != nil {
        return 0, result.Error
    }

    // Invalidar cache si se eliminaron registros
    if result.RowsAffected > 0 {
        InvalidateTopicsCache()
    }

    return result.RowsAffected, nil
}
