package auth

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"services01/pkg/presets"
)

type handler struct {
	DB *gorm.DB
}

func RegRoutes(r *gin.Engine, c *presets.Config) {
	h := &handler{
		DB: c.DB,
	}
	routers := r.Group("/api/v1/auth")
	routers.POST("/add_usr", h.AddUsr)
	routers.GET("/token", h.GetTkn)
}

// test
