package objects

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/models"
	"time"
)

func (h handler) GetAccidents(c *gin.Context) {
	var accidents []models.PredictionAccident
	if h.DB.Find(&accidents).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &accidents)
}

func (h handler) GetAccident(c *gin.Context) {
	id := c.Param("id")
	var accident models.PredictionAccident
	if h.DB.Where("id = ?", id).Find(&accident).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &accident)
}

func (h handler) UpdateAccident(c *gin.Context) {
	var accidentStruct struct {
		ObjConsumerStationId uint64    `json:"obj_consumer_station_id"`
		ObjConsumerId        uint64    `json:"obj_consumer_id"`
		IsAccident           bool      `json:"is_accident"`
		Percent              float64   `json:"percent"`
		IsApproved           bool      `json:"is_approved"`
		IsActual             bool      `json:"is_actual"`
		Created              time.Time `json:"created"`
		Closed               time.Time `json:"closed"`
	}
	c.Bind(&accidentStruct)
	var accident models.PredictionAccident
	id := c.Param("id")

	if err := h.DB.Select("*").Where("id = ?", id).Find(&accident).Error; err != nil {
		c.JSON(http.StatusNotFound, "Accident not found")
		return
	}

	h.DB.Model(&accident).Updates(accidentStruct)
	c.JSON(http.StatusOK, &accident)
}
