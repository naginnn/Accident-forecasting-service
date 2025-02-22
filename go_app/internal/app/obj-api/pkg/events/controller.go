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
	routers.POST("/events", middlewares.RoleChecker(h.UpdateEvent, "rw"))
	routers.GET("/events/:id", middlewares.RoleChecker(h.GetEventsByConsumerId, "rw,ro"))
	routers.GET("/events_counter/:id", middlewares.RoleChecker(h.GetEventsCounterByConsumerId, "rw,ro"))
}
