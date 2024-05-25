package config

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/models"
)

// Read
func (h handler) GetWeatherConditions(c *gin.Context) {
	var weatherConditions []models.WeatherCondition
	if h.DB.Find(&weatherConditions).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "WeatherConditions not found")
		return
	}
	c.JSON(http.StatusOK, &weatherConditions)
}

func (h handler) GetWeatherCondition(c *gin.Context) {
	id := c.Param("id")
	var weatherCondition models.WeatherCondition
	if h.DB.Select("*").Where("id = ?", id).Find(&weatherCondition).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "WeatherCondition not found")
		return
	}
	c.JSON(http.StatusOK, &weatherCondition)
}

// Update
func (h handler) UpdateWeatherCondition(c *gin.Context) {
	id := c.Param("id")
	var weatherCondition models.WeatherCondition
	if h.DB.Select("*").Where("id = ?", id).Find(&weatherCondition).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "WeatherCondition not found")
		return
	}

	// check data_param
	type weatherStruct struct {
		Description string  `json:"description"`
		K           float64 `json:"k"`
	}
	var weather weatherStruct
	if err := c.ShouldBindJSON(&weather); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	h.DB.Model(&weatherCondition).Updates(weather)
	c.JSON(http.StatusOK, &weather)
}

// Delete
func (h handler) DeleteWeatherCondition(c *gin.Context) {
	id := c.Param("id")
	var weatherCondition models.WeatherCondition
	if h.DB.Select("*").Where("id = ?", id).Find(&weatherCondition).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "WeatherCondition not found")
		return
	}
	if err := h.DB.Delete(&weatherCondition).Error; err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}
	c.JSON(http.StatusOK, &weatherCondition)
}
