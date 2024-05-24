package objects

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
	routers.GET("/table_view", middlewares.RoleChecker(h.GetTableView, "ro,rw"))
	//GetTableView
	// Areas
	//GetAreas
	routers.GET("/areas", middlewares.RoleChecker(h.GetAreas, "ro,rw"))
	// Source Station
	routers.GET("/source-stations", middlewares.RoleChecker(h.GetSourceStations, "ro,rw"))
	routers.GET("/source-stations/:id", middlewares.RoleChecker(h.GetSourceStation, "ro,rw"))

	// Consumer Station
	routers.GET("/consumer-stations", middlewares.RoleChecker(h.GetConsumerStations, "ro,rw"))
	routers.GET("/consumer-stations/:id", middlewares.RoleChecker(h.GetConsumerStation, "ro,rw"))

	// Consumer routers
	routers.GET("/consumers", middlewares.RoleChecker(h.GetConsumers, "ro,rw"))
	routers.GET("/consumers/:id", middlewares.RoleChecker(h.GetConsumer, "ro,rw"))

	// Accidents
	routers.GET("/accidents", middlewares.RoleChecker(h.GetAccidents, "ro,rw"))
	routers.GET("/accidents/:id", middlewares.RoleChecker(h.GetAccident, "ro,rw"))
	routers.PUT("/accidents/update", middlewares.RoleChecker(h.UpdateAccident, "rw"))

	// Events
	routers.GET("/events", middlewares.RoleChecker(h.GetEvents, "ro"))
	routers.GET("/events/:id", middlewares.RoleChecker(h.GetEvent, "ro"))
	routers.PATCH("/events/:id", middlewares.RoleChecker(h.UpdateEvent, "rw"))
}
