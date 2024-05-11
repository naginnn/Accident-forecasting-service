package temp

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/weather"
)

func (h handler) CalculateWeatherFall(c *gin.Context) {
	//err := weather.UpdateTempDataArea(h.DB)
	//if err != nil {
	//	c.JSON(http.StatusNotModified, nil)
	//	return
	//}
	err := weather.CalculateFallTemp(h.DB)
	if err != nil {
		c.JSON(http.StatusNotModified, nil)
		return
	}
	c.JSON(http.StatusOK, nil)
}

func (h handler) UpdateAreaForecasts(c *gin.Context) {
	err := weather.UpdateTempDataArea(h.DB)
	if err != nil {
		c.JSON(http.StatusNotModified, nil)
		return
	}
	//err := weather.CalculateFallTemp(h.DB)
	//if err != nil {
	//	c.JSON(http.StatusNotModified, nil)
	//	return
	//}
	//c.JSON(http.StatusOK, nil)
}
