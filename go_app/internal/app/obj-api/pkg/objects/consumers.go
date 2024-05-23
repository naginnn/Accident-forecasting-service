package objects

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"log"
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
	var consumerStation models.ObjConsumerStation
	var sourceStation models.ObjSourceStation

	err := h.DB.
		Preload("WeatherFall", func(tx *gorm.DB) *gorm.DB {
			return tx.Last(&models.WeatherConsumerFall{})
		}).
		Preload("Events", func(tx *gorm.DB) *gorm.DB {
			//return tx.Raw(`select * from event_consumers ec order by ec.created`).Scan(&models.EventConsumer{})
			return tx.Order("Created desc")
		}).
		Where("id = ?", id).Find(&consumer).Error

	if err != nil {
		log.Println(err)
	}
	err = h.DB.
		//Preload("Consumers").
		Preload("Consumers").
		Preload("SourceStations").
		Where("id = ?", consumer.ObjConsumerStationId).Find(&consumerStation).Error
	if err != nil {
		log.Println(err)
	}
	err = h.DB.Where("id = ?", consumerStation.SourceStations[0].ID).Find(&sourceStation).Error
	if err != nil {
		log.Println(err)
	}

	c.JSON(http.StatusOK, gin.H{
		"consumer":         &consumer,
		"source_station":   &sourceStation,
		"consumer_station": &consumerStation,
	})
}
