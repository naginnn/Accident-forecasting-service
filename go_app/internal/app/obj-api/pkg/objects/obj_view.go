package objects

import (
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
	"log"
	"net/http"
	"services01/pkg/models"
)

func (h handler) GetObjView(c *gin.Context) {
	id := c.Param("id")
	var warnConsumer models.ObjConsumer
	var warnConsumerStation models.ObjConsumerStation

	err := h.DB.
		Preload("WeatherFall", func(tx *gorm.DB) *gorm.DB {
			return tx.Last(&models.WeatherConsumerFall{})
		}).
		Preload("Events", func(tx *gorm.DB) *gorm.DB {
			return tx.Order("Created desc")
		}).
		Where("id = ?", id).Find(&warnConsumer).Error

	err = h.DB.Preload("SourceStations").Where("id = ?", warnConsumer.ObjConsumerStationId).Find(&warnConsumerStation).Error

	var dependentConsumers []DependentConsumer
	err = h.DB.Raw(`
select c.id, c.obj_consumer_station_id, c.name, c.address, c.coordinates, 
       ecf.source, ecf.description, ecf.probability, ecf.is_approved, ecf.is_closed
from public.obj_consumers c left join (select ecc.obj_consumer_id, max(ecc.id) as id from public.event_consumers as ecc group by obj_consumer_id) ec on ec.obj_consumer_id = c.id
         left join public.event_consumers ecf on ecf.id = ec.id
		join public.obj_consumer_stations cs on cs.id = c.obj_consumer_station_id
where cs.id = ?
`, warnConsumerStation.ID).Scan(&dependentConsumers).Error
	if err != nil {
		log.Println(err)
	}
	c.JSON(http.StatusOK, gin.H{
		"dependent_consumers":   &dependentConsumers,
		"warn_consumer":         &warnConsumer,
		"warn_consumer_station": &warnConsumerStation,
	})
}

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
