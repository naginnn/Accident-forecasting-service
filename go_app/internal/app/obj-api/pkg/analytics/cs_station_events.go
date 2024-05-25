package analytics

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

type CsStationEventsCount struct {
	Name        string `json:"name"`
	EventsCount string `json:"events_count"`
}

func (h handler) GetCsStationEvents(c *gin.Context) {
	var eventsCount []CsStationEventsCount
	if h.DB.Raw(`select cs.name, count(ec.id) as events_count
from obj_consumer_stations cs
       left join public.obj_consumers oc on cs.id = oc.obj_consumer_station_id
       left join public.event_consumers ec on oc.id = ec.obj_consumer_id
group by cs.name order by count(ec.id) desc;`).Scan(&eventsCount).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &eventsCount)
}
