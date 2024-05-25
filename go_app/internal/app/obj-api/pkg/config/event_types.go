package config

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm/clause"
	"log"
	"net/http"
	"services01/pkg/models"
)

// Create
func (h handler) CreateEventsTypes(c *gin.Context) {
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

// Read
func (h handler) GetEventsTypes(c *gin.Context) {
	var events []models.EventType
	if h.DB.Find(&events).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "Events not found")
		return
	}
	c.JSON(http.StatusOK, &events)
}

// Update
func (h handler) UpdateEventsTypes(c *gin.Context) {
	var eventType models.EventType
	if err := c.ShouldBindJSON(&eventType); err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	if err := h.DB.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "name"}},
		DoUpdates: clause.AssignmentColumns([]string{"k"}),
	}).Updates(&eventType).Error; err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}
	c.JSON(http.StatusOK, &eventType)
}

// Delete
func (h handler) DeleteEventsTypes(c *gin.Context) {
	var eventType models.EventType
	if err := c.ShouldBindJSON(&eventType); err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	if err := h.DB.Delete(&eventType).Error; err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, "ok")
}
