package objects

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
	var consumerWarn, consumersDep []models.ObjConsumer
	if h.DB.Where("id = ?", objConsumerStationId).
		//Preload("Weather", func(tx *gorm.DB) *gorm.DB {
		//	return tx.Last(&models.WeatherArea{})
		//}).
		Preload("SourceStations").
		Preload("Consumers.WeatherFall", func(tx *gorm.DB) *gorm.DB {
			//return tx.Order("Created desc")
			return tx.Last(&models.WeatherConsumerFall{})
		}).
		Preload("Consumers.Events", func(tx *gorm.DB) *gorm.DB {
			//return tx.Where("is_closed = ? ", false)
			return tx.Order("Created desc").Limit(5)
			//return tx.Last(&models.WeatherConsumerFall{})
		}).
		Preload("Consumers.WallMaterial").
		Find(&consumerStation).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	var area models.LocationArea
	if h.DB.Where("id = ?", consumerStation.LocationAreaId).
		Preload("Weather", func(tx *gorm.DB) *gorm.DB {
			return tx.Last(&models.WeatherArea{})
		}).
		Find(&area).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	flag := false
	var weather Weather
	for _, forecast := range area.Weather[0].TempInfo.Forecasts {
		if flag {
			break
		}
		tNow := time.Now().Format("2006-01-02")
		tForecast := time.Unix(int64(forecast.DateTs), 0).Format("2006-01-02")
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

	area.Weather = nil
	consumersDep = consumerStation.Consumers
	consumerStation.Consumers = nil
	sourceStations := consumerStation.SourceStations
	consumerStation.SourceStations = nil

	for _, cons := range consumersDep {
		for _, event := range cons.Events {
			if !event.IsClosed {
				consumerWarn = append(consumerWarn, cons)
				break
			}
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"weather":           &weather,
		"area":              &area,
		"consumer_stations": &consumerStation,
		"consumers_dep":     &consumersDep,
		"consumer_warn":     &consumerWarn,
		"source_stations":   &sourceStations,
	})
}

//q := `select
//    ld.id ld_id, ld.name ld_name,
//    la.id la_id, la.name la_name, la.coordinates la_coordinates,
//    ss.id ss_id, ss.name ss_name, ss.address ss_address, ss.coordinates ss_coordinates,
//    ocs.id cs_id, ocs.name cs_name, ocs.address cs_address, ocs.coordinates cs_coordinates,
//    ecf.id temp_id, ecf.temp_info temp_info, ecf.created temp_created
//from obj_consumer_stations ocs
//    join location_areas la on la.id = ocs.location_area_id
//    join location_districts ld on la.location_district_id = ld.id
//    join public.obj_source_consumer_stations scs on ocs.id = scs.obj_consumer_station_id
//    join public.obj_source_stations ss on ss.id = scs.obj_source_station_id
//    left join (select wa.location_area_id, max(wa.id) as id from public.weather_areas as wa group by location_area_id) waa on waa.location_area_id = la.id
//    left join public.weather_areas ecf on ecf.id = waa.id
//where ocs.id = ?`
//
//if h.DB.Raw(q, objConsumerStationId).Scan(&data).RowsAffected == 0 {
//c.JSON(http.StatusNotFound, "not found")
//return
//}
//c.JSON(http.StatusOK, gin.H{"Lala": 1})

//
//func (h handler) GetObjView(c *gin.Context) {
//	//objConsumerStationId := c.Param("obj_consumer_station_id")
//	//var warnConsumerStation models.ObjConsumerStation
//	//err := h.DB.
//	//	Preload("SourceStations").
//	//	Preload("Consumers").
//	//	Preload("Consumers.WeatherFall", func(tx *gorm.DB) *gorm.DB {
//	//		return tx.Order("Created desc")
//	//		//return tx.Last(&models.WeatherConsumerFall{})
//	//	}).
//	//	Preload("Consumers.Events", func(tx *gorm.DB) *gorm.DB {
//	//		return tx.
//	//			Where("is_closed = ?", false).
//	//			Select("ObjConsumerId", "*")
//	//		//return tx.Where("", &consumerEvents).Order("Created desc")
//	//	}).
//	//	Where("id = ?", objConsumerStationId).Find(&warnConsumerStation).Error
//	//if err != nil {
//	//	log.Println(err)
//	//}
//	//c.JSON(http.StatusOK, &warnConsumerStation)
//	//var lala Lala
//	//lala.Name = "dsadsa"
//	c.JSON(http.StatusOK, gin.H{"Lala": 1})
//	//	var warnConsumer models.ObjConsumer
//	//	err := h.DB.
//	//		Preload("WeatherFall", func(tx *gorm.DB) *gorm.DB {
//	//			return tx.Last(&models.WeatherConsumerFall{})
//	//		}).
//	//		Preload("Events", func(tx *gorm.DB) *gorm.DB {
//	//			return tx.Order("Created desc")
//	//		}).
//	//		Where("id = ?", id).Find(&warnConsumer).Error
//	//
//	//	err = h.DB.Preload("SourceStations").Where("id = ?", warnConsumer.ObjConsumerStationId).Find(&warnConsumerStation).Error
//	//
//	//	var dependentConsumers []DependentConsumer
//	//	err = h.DB.Raw(`
//	//select c.id, c.obj_consumer_station_id, c.name, c.address, c.coordinates,
//	//       ecf.source, ecf.description, ecf.probability, ecf.is_approved, ecf.is_closed
//	//from public.obj_consumers c left join (select ecc.obj_consumer_id, max(ecc.id) as id from public.event_consumers as ecc group by obj_consumer_id) ec on ec.obj_consumer_id = c.id
//	//         left join public.event_consumers ecf on ecf.id = ec.id
//	//		join public.obj_consumer_stations cs on cs.id = c.obj_consumer_station_id
//	//where cs.id = ?
//	//`, warnConsumerStation.ID).Scan(&dependentConsumers).Error
//	//	if err != nil {
//	//		log.Println(err)
//	//	}
//	//	c.JSON(http.StatusOK, gin.H{
//	//		"dependent_consumers":   &dependentConsumers,
//	//		"warn_consumer":         &warnConsumer,
//	//		"warn_consumer_station": &warnConsumerStation,
//	//	})
//}

type DependentConsumer struct {
	ID          uint64  `json:"id"`
	Name        string  `json:"name"`
	Address     string  `json:"address"`
	Coordinates string  `json:"coordinates"`
	Source      string  `json:"source"`
	Description string  `json:"description"`
	Probability float64 `json:"probability"`
	IsApproved  bool    `json:"is_approved"`
	IsClosed    bool    `json:"is_closed"`
	IsWarning   bool    `json:"is_warning"`
}
