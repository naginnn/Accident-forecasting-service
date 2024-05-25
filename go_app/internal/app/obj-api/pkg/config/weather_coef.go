package config

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm/clause"
	"net/http"
	"services01/pkg/models"
)

// Read
func (h handler) GetWeatherCondition(c *gin.Context) {
	var weatherCondition []models.WeatherCondition
	if h.DB.Find(&weatherCondition).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "WeatherCondition not found")
		return
	}

	c.JSON(http.StatusOK, &weatherCondition)
}

// Update
func (h handler) UpdateWeatherCondition(c *gin.Context) {
	var weatherCondition models.WeatherCondition
	if err := c.ShouldBindJSON(&weatherCondition); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.DB.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "name"}},
		DoUpdates: clause.AssignmentColumns([]string{"k"}),
	}).Updates(&weatherCondition).Error; err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, &weatherCondition)
}
