package temp

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
	routers := r.Group("/api/v1/obj")
	routers.POST("/weather/calculate", h.CalculateWeatherFall)
	routers.POST("/weather/calculate_go", h.CalculateWeatherFallGo)
	routers.POST("/weather/update", h.UpdateAreaForecasts)
}
