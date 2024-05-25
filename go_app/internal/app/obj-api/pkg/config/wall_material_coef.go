package config

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm/clause"
	"net/http"
	"services01/pkg/models"
)

// Create
func (h handler) CreateWallMaterials(c *gin.Context) {
	var materialWall models.MaterialWall
	if err := c.ShouldBindJSON(&materialWall); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.DB.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "name"}},
		DoUpdates: clause.AssignmentColumns([]string{"k"}),
	}).Create(&materialWall).Error; err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}
	c.JSON(http.StatusOK, &materialWall)
}

// Read
func (h handler) GetWallMaterials(c *gin.Context) {
	var materialWall []models.MaterialWall
	if h.DB.Order("Id").Find(&materialWall).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "Materials not found")
		return
	}
	c.JSON(http.StatusOK, &materialWall)
}

// Update
func (h handler) UpdateWallMaterials(c *gin.Context) {
	var materialWall models.MaterialWall
	if err := c.ShouldBindJSON(&materialWall); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.DB.Clauses(clause.OnConflict{
		Columns:   []clause.Column{{Name: "name"}},
		DoUpdates: clause.AssignmentColumns([]string{"k"}),
	}).Updates(&materialWall).Error; err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, &materialWall)
}

// Delete
func (h handler) DeleteWallMaterials(c *gin.Context) {
	var materialWall models.MaterialWall
	if err := c.ShouldBindJSON(&materialWall); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if err := h.DB.Delete(&materialWall).Error; err != nil {
		c.JSON(http.StatusBadRequest, err)
		return
	}

	c.JSON(http.StatusOK, "ok")
}
