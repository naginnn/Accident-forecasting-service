package view

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

func (h handler) GetTableView(c *gin.Context) {
	var result []struct {
		SourceStationId          int64  `gorm:"source_station_id"`
		SourceStationName        string `json:"source_station_name"`
		SourceStationAddress     string `json:"source_station_address"`
		SourceStationCoordinates string `json:"source_station_coordinates"`

		ConsumerStationId          int64  `json:"consumer_station_id"`
		ConsumerStationName        string `json:"consumer_station_name"`
		ConsumerStationAddress     string `json:"consumer_station_address"`
		ConsumerStationCoordinates string `json:"consumer_station_coordinates"`

		LocationDistrictConsumerId   int64  `json:"location_district_consumer_id"`
		LocationDistrictConsumerName string `json:"location_district_consumer_name"`

		LocationAreaConsumerId          int64  `json:"location_area_consumer_id"`
		LocationAreaConsumerName        string `json:"location_area_consumer_name"`
		LocationAreaConsumerCoordinates string `json:"location_area_consumer_coordinates"`

		ConsumerId          int64  `json:"consumer_id"`
		ConsumerName        string `json:"consumer_name"`
		ConsumerAddress     string `json:"consumer_address"`
		ConsumerCoordinates string `json:"consumer_coordinates"`

		Source      string  `json:"source"`
		Description string  `json:"description"`
		Probability float64 `json:"probability"`
		IsApproved  bool    `json:"is_approved"`
		IsClosed    bool    `json:"is_closed"`
		IsWarning   bool    `json:"is_warning"`
	}

	q := `select
    ss.id source_station_id, ss.name source_station_name, ss.address source_station_address, ss.coordinates source_station_coordinates,
    cs.id consumer_station_id, cs.name consumer_station_name, cs.address consumer_station_address, cs.coordinates consumer_station_coordinates,
    ld.id location_district_consumer_id, ld.name location_district_consumer_name,
    la.id location_area_consumer_id, la.name location_area_consumer_name, la.coordinates location_area_consumer_coordinates,
    c.id consumer_id, c.name consumer_name, c.address consumer_address, c.coordinates consumer_coordinates,
    ecf.source, ecf.description, ecf.probability, ecf.is_approved, ecf.is_closed,
    (SELECT EXISTS(SELECT true FROM public.event_consumers WHERE id = ec.id and is_closed = false)) as is_warning
from obj_consumers as c
         join public.location_districts ld on ld.id = c.location_district_id
         join public.location_areas la on ld.id = c.location_area_id
         join public.obj_consumer_stations cs on cs.id = c.obj_consumer_station_id
         join public.obj_source_consumer_stations scs on cs.id = scs.obj_consumer_station_id
         join public.obj_source_stations ss on ss.id = scs.obj_source_station_id
         left join (select ecc.obj_consumer_id, max(ecc.id) as id from public.event_consumers as ecc group by obj_consumer_id) ec on ec.obj_consumer_id = cs.id
         left join public.event_consumers ecf on ecf.id = ec.id
order by is_warning desc;`

	if h.DB.Raw(q).Scan(&result).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &result)
}
