package objects

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm/clause"
	"log"
	"net/http"
	"services01/pkg/models"
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
	var accident models.PredictionAccident
	err := c.Bind(&accident)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusNotModified, err)
		return
	}
	err = h.DB.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "id"}},
		DoUpdates: clause.AssignmentColumns([]string{"is_approved", "is_closed"}),
	}).Create(&accident).Error
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusNotModified, err)
		return
	}
	c.JSON(http.StatusAccepted, "updated")
}
