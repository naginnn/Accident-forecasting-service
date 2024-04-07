package objects

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func (h handler) GetObj(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"Hello": "world!"})

}
