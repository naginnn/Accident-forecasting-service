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
	routers := r.Group("/api/v1/obj/objects")

	// Source Station
	routers.GET("/source-stations", middlewares.RoleChecker(h.GetSourceStations, "ro,rw"))
	routers.GET("/source-stations/:id", middlewares.RoleChecker(h.GetSourceStation, "ro,rw"))

	// Consumer Station
	routers.GET("/consumer-stations", middlewares.RoleChecker(h.GetConsumerStations, "ro,rw"))
	routers.GET("/consumer-stations/:id", middlewares.RoleChecker(h.GetConsumerStation, "ro,rw"))

	// Consumer
	routers.GET("/consumers", middlewares.RoleChecker(h.GetConsumers, "ro,rw"))
	routers.GET("/consumers/:id", middlewares.RoleChecker(h.GetConsumer, "ro,rw"))

}
