package analytics

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/models"
)

func (h handler) GetModelInfo(c *gin.Context) {
	var modelInfo models.ModelInfo
	if h.DB.Find(&modelInfo).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &modelInfo)
}
