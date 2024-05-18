package objects

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"net/http"
	"services01/pkg/models"
)

func (h handler) GetConsumers(c *gin.Context) {
	var consumers []models.ObjConsumer
	if h.DB.Find(&consumers).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &consumers)
}

func (h handler) GetConsumer(c *gin.Context) {
	id := c.Param("id")
	var consumer models.ObjConsumer
	if h.DB.
		Preload("WeatherFall", func(tx *gorm.DB) *gorm.DB {
			return tx.Last(&models.WeatherConsumerFall{})
		}).
		Preload("Accidents", func(tx *gorm.DB) *gorm.DB {
			return tx.Last(&models.PredictionAccident{})
		}).
		Preload("Events", func(tx *gorm.DB) *gorm.DB {
			return tx.Last(&models.EventConsumer{})
		}).
		Where("id = ?", id).Find(&consumer).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}

	c.JSON(http.StatusOK, &consumer)
}
