package config

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/models"
)

// Create
func (h handler) CreateEventsTypes(c *gin.Context) {

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

}

// Delete
func (h handler) DeleteEventsTypes(c *gin.Context) {

}
