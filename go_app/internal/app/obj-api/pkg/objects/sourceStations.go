package objects

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/models"
)

func (h handler) GetSourceStations(c *gin.Context) {
	var sourceStation []models.ObjSourceStation
	if h.DB.Find(&sourceStation).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &sourceStation)
}

func (h handler) GetSourceStation(c *gin.Context) {
	id := c.Param("id")
	var sourceStation *models.ObjSourceStation
	if h.DB.Where("id = ?", id).Find(&sourceStation).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &sourceStation)
}
