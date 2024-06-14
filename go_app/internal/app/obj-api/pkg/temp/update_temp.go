package temp

import (
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"services01/pkg/weather"
	"time"
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

func (h handler) CalculateWeatherFallGo(c *gin.Context) {
	go func() {
		for {
			err := weather.CalculateFallTemp(h.DB)
			if err != nil {
				log.Println(err)
			}
			time.Sleep(1 * time.Hour)
		}
	}()
	c.JSON(http.StatusOK, nil)
}

//go func() {
//	time.Sleep(4 * time.Minute)
//	err := weather.UpdateTempDataArea(c.DB)
//	if err != nil {
//		log.Println(err)
//	}
//	for {
//		err = weather.CalculateFallTemp(c.DB)
//		if err != nil {
//			log.Println(err)
//		}
//		time.Sleep(2 * time.Minute)
//	}
//}()
