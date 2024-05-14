package objects

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/models"
)

func (h handler) GetConsumerStations(c *gin.Context) {
	var consumerStation []models.ObjConsumerStation
	if h.DB.Find(&consumerStation).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &consumerStation)
}

func (h handler) GetConsumerStation(c *gin.Context) {
	id := c.Param("id")
	var consumerStation models.ObjConsumerStation
	if h.DB.Where("id = ?", id).Find(&consumerStation).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &consumerStation)
}
