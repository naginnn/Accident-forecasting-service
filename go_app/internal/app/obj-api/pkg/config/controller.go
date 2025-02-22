package config

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
	routers := r.Group("/api/v1/obj/config")
	// event_types
	routers.GET("/events", middlewares.RoleChecker(h.GetEventsTypes, "rw"))
	routers.PUT("/events", middlewares.RoleChecker(h.CreateEventsTypes, "rw"))
	routers.DELETE("/events", middlewares.RoleChecker(h.DeleteEventsTypes, "rw"))
	routers.POST("/events", middlewares.RoleChecker(h.UpdateEventsTypes, "rw"))

	//wall materials
	routers.GET("/wall_materials", middlewares.RoleChecker(h.GetWallMaterials, "rw"))
	routers.PUT("/wall_materials", middlewares.RoleChecker(h.CreateWallMaterials, "rw"))
	routers.DELETE("/wall_materials", middlewares.RoleChecker(h.DeleteWallMaterials, "rw"))
	routers.POST("/wall_materials", middlewares.RoleChecker(h.UpdateWallMaterials, "rw"))

	// weather condition
	routers.GET("/weather_conditions", middlewares.RoleChecker(h.GetWeatherCondition, "rw"))
	routers.POST("/weather_conditions", middlewares.RoleChecker(h.UpdateWeatherCondition, "rw"))
}
