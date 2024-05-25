package config

import (
	"github.com/gin-gonic/gin"
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

}
