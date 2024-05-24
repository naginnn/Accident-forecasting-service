package events

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"services01/pkg/middlewares"
	"services01/pkg/presets"
)

type handler struct {
	DB *gorm.DB
}

func RegRoutes(r *gin.Engine, c *presets.Config) {
	h := &handler{
		DB: c.DB,
	}
	routers := r.Group("/api/v1/obj")
	// TableView
	routers.POST("/events", middlewares.RoleChecker(h.UpdateEvent, "rw"))
}
