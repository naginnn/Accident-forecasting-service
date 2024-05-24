package objects

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm/clause"
	"log"
	"net/http"
	"services01/pkg/models"
)

func (h handler) CreateEventType(c *gin.Context) {
	// check last ID
	var lastVersion struct {
		ID int
	}
	lastErr := h.DB.Table("event_types").Last(&lastVersion)
	if lastErr != nil {
		log.Println(lastErr)
	}

	var nameStruct struct {
		EventName string `json:"event_name"`
	}
	c.Bind(&nameStruct)
	var eventType models.EventType
	eventType.ID = uint64(lastVersion.ID + 1)
	eventType.EventName = nameStruct.EventName

	err := h.DB.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "event_name"}},
		DoUpdates: clause.AssignmentColumns([]string{"event_name"}),
	}).Create(&eventType).Error
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusNotFound, "Can't create or update field")
		return
	}
	c.JSON(http.StatusOK, &eventType)
}

func (h handler) GetEventTypes(c *gin.Context) {
	var eventTypes []models.EventType
	if h.DB.Find(&eventTypes).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "Event Types not found")
		return
	}
	c.JSON(http.StatusOK, &eventTypes)
}

func (h handler) GetEventType(c *gin.Context) {
	id := c.Param("id")
	var eventType models.EventType
	if h.DB.Select("*").
		Where("id = ?", id).Find(&eventType).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "Event not found")
		return
	}
	c.JSON(http.StatusOK, &eventType)
}

func (h handler) UpdateEventType(c *gin.Context) {
	// find event
	id := c.Param("id")
	var eventType models.EventType
	if h.DB.Select("*").Where("id = ?", id).Find(&eventType).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "Event Type not found")
		return
	}

	// check data_param
	type nameStruct struct {
		EventName string `json:"event_name"`
	}
	var name nameStruct
	if err := c.ShouldBindJSON(&name); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	h.DB.Model(&eventType).Updates(name)
	c.JSON(http.StatusOK, &name)
}
