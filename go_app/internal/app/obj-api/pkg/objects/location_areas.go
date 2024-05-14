package objects

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
	"log"
	"net/http"
	"services01/pkg/models"
)

func (h handler) GetAreas(c *gin.Context) {
	var areas []models.LocationArea
	err := h.DB.
		Preload("Weather", func(tx *gorm.DB) *gorm.DB {
			return tx.Last(&models.WeatherArea{})
		}).
		//Preload("Consumers").Find(&areas).Error
		//Preload("Consumers.WeatherFall").
		Preload(clause.Associations).Find(&areas).Error

	if err != nil {
		log.Println(err)
		return
	}
	c.JSON(http.StatusOK, &areas)
}
