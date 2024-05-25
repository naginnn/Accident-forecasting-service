package analytics

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
	routers := r.Group("/api/v1/obj/analytics")
	routers.GET("/model_info", middlewares.RoleChecker(h.GetModelInfo, "ro,rw"))
	routers.GET("/cs_events", middlewares.RoleChecker(h.GetCsEvents, "ro,rw"))
	routers.GET("/cs_station_events", middlewares.RoleChecker(h.GetCsStationEvents, "ro,rw"))
}
