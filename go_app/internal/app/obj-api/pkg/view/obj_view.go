package view

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"net/http"
	"services01/pkg/models"
	"time"
)

type Weather struct {
	Temp      float64 `json:"temp"`
	WindSpeed float64 `json:"wind_speed"`
	WindDir   string  `json:"wind_dir"`
	Humidity  float64 `json:"humidity"`
	Condition string  `json:"condition"`
}

func (h handler) GetObjView(c *gin.Context) {
	objConsumerStationId := c.Param("obj_consumer_station_id")
	var consumerStation models.ObjConsumerStation
	var sourceStations []models.ObjSourceStation
	var consumers []models.ObjConsumer
	var area models.LocationArea

	//if h.DB.Where("obj_consumer_station_id = ?", objConsumerStationId).
	//	Preload("Events").
	//	Preload("Events", func(tx *gorm.DB) *gorm.DB {
	//		return tx.Raw("select ec.* FROM public.event_consumers as ec " +
	//			"JOIN (SELECT MAX(id) AS id, obj_consumer_id " +
	//			"FROM event_consumers WHERE 1 IN(1) GROUP BY obj_consumer_id) sub " +
	//			"USING(id, obj_consumer_id) JOIN public.obj_consumers c " +
	//			"ON c.id = ec.obj_consumer_id where c.obj_consumer_station_id = '" + objConsumerStationId + "' ORDER BY ec.id DESC;")
	//	}).
	//	Preload("WeatherFall", func(tx *gorm.DB) *gorm.DB {
	//		return tx.Raw("select ec.* FROM weather_consumer_falls as ec " +
	//			"JOIN (SELECT MAX(id) AS id, obj_consumer_id " +
	//			"FROM weather_consumer_falls WHERE 1 IN(1) GROUP BY obj_consumer_id) sub " +
	//			"USING(id, obj_consumer_id) JOIN obj_consumers c " +
	//			"ON c.id = ec.obj_consumer_id where c.obj_consumer_station_id = '" + objConsumerStationId + "' ORDER BY ec.id DESC;")
	//	}).
	//	Preload("WallMaterial").
	//	Find(&consumers).RowsAffected == 0 {
	//	c.JSON(http.StatusNotFound, "not found")
	//	return
	//}
	//var weatherFall []models.WeatherConsumerFall
	//q := "select ec.* FROM weather_consumer_falls as ec " +
	//	"JOIN (SELECT MAX(id) AS id, obj_consumer_id " +
	//	"FROM weather_consumer_falls WHERE 1 IN(1) GROUP BY obj_consumer_id) sub " +
	//	"USING(id, obj_consumer_id) JOIN obj_consumers c " +
	//	"ON c.id = ec.obj_consumer_id where c.obj_consumer_station_id = '" + objConsumerStationId + "' ORDER BY ec.id DESC;"
	//err := h.DB.Raw(q).Scan(&weatherFall).Error
	//if err != nil {
	//	fmt.Println(err)
	//}
	//
	//var newConsumers []models.ObjConsumer
	//for _, consumer := range consumers {
	//	q := "select ec.* " +
	//		"FROM public.event_consumers as ec " +
	//		"JOIN (SELECT MAX(id) AS id, obj_consumer_id " +
	//		"FROM event_consumers WHERE 1 IN(1) " +
	//		"GROUP BY obj_consumer_id) sub " +
	//		"USING(id, obj_consumer_id) " +
	//		"JOIN public.obj_consumers c ON c.id = ec.obj_consumer_id where c.id = " + strconv.FormatUint(consumer.ID, 10) + " ORDER BY ec.id DESC;"
	//	err := h.DB.Raw(q).Scan(&consumer.Events).Error
	//	if err != nil {
	//		fmt.Println(err)
	//	}
	//	for _, whFall := range weatherFall {
	//		if whFall.ObjConsumerId == consumer.ID {
	//			consumer.WeatherFall = append(consumer.WeatherFall, whFall)
	//			break
	//		}
	//	}
	//	//consumer.WeatherFall = weatherFall
	//	newConsumers = append(newConsumers, consumer)
	//	if err != nil {
	//		fmt.Println(err)
	//	}
	//}
	//
	q := "select * from public.obj_source_stations " +
		"join public.obj_source_consumer_stations oscs on obj_source_stations.id = oscs.obj_source_station_id " +
		"where oscs.obj_consumer_station_id = '" + objConsumerStationId + "'"
	h.DB.Raw(q).Scan(&sourceStations)

	if h.DB.Where("id = ?", objConsumerStationId).
		//Preload("SourceStations").
		Preload("Weather", func(tx *gorm.DB) *gorm.DB {
			return tx.Last(&models.WeatherArea{})
		}).
		//Preload("SourceStations").
		Preload("Consumers.Events", func(tx *gorm.DB) *gorm.DB {
			return tx.Raw("select ec.* FROM event_consumers as ec " +
				"JOIN (SELECT MAX(id) AS id, obj_consumer_id " +
				"FROM event_consumers WHERE 1 IN(1) GROUP BY obj_consumer_id) sub " +
				"USING(id, obj_consumer_id) JOIN obj_consumers c " +
				"ON c.id = ec.obj_consumer_id where c.obj_consumer_station_id = '" + objConsumerStationId + "' ORDER BY ec.id DESC;")
		}).
		Preload("Consumers.WeatherFall", func(tx *gorm.DB) *gorm.DB {
			return tx.Raw("select ec.* FROM weather_consumer_falls as ec " +
				"JOIN (SELECT MAX(id) AS id, obj_consumer_id " +
				"FROM weather_consumer_falls WHERE 1 IN(1) GROUP BY obj_consumer_id) sub " +
				"USING(id, obj_consumer_id) JOIN obj_consumers c " +
				"ON c.id = ec.obj_consumer_id where c.obj_consumer_station_id = '" + objConsumerStationId + "' ORDER BY ec.id DESC;")
		}).
		Preload("Consumers.WallMaterial").
		//Preload("SourceStations").
		Find(&consumerStation).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}

	if h.DB.Where("id = ?", consumerStation.LocationAreaId).
		//Preload("Weather").
		Preload("Weather", func(tx *gorm.DB) *gorm.DB {
			return tx.Last(&models.WeatherArea{})
		}).
		Find(&area).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	flag := false
	var weather Weather
	if len(area.Weather) > 0 {
		for _, forecast := range area.Weather[0].TempInfo.Forecasts {
			if flag {
				break
			}
			tNow := time.Now().Format("2006-01-02")
			tForecast := forecast.Date
			if tNow == tForecast {
				if tNow == tForecast {
					hNow := time.Now()
					for _, data := range forecast.Hours {
						hForecast := time.Unix(int64(data.HourTs), 0)
						if hNow.Hour() == hForecast.Hour() {
							weather.WindSpeed = data.WindSpeed
							weather.Humidity = float64(data.Humidity)
							weather.WindDir = data.WindDir
							weather.Condition = data.Condition
							weather.Temp = float64(data.Temp)
							flag = true
							break
						}
					}
				}
			}
		}
	}

	//var sourceStations []*models.ObjSourceStation
	area.Weather = nil
	consumers = consumerStation.Consumers
	consumerStation.Consumers = nil
	//sourceStations = consumerStation.SourceStations
	//consumerStation.SourceStations = nil

	c.JSON(http.StatusOK, gin.H{
		"weather":           &weather,
		"area":              &area,
		"consumer_stations": &consumerStation,
		"consumers_dep":     &consumers,
		//"consumers_dep":     &newConsumers,
		//"consumer_warn":     &consumerWarn,
		//"source_stations": &sourceStation,
		//"source_stations": &consumerStation.SourceStations,
		"source_stations": &sourceStations,
	})
}
