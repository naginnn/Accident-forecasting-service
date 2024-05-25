package analytics

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

type CsEventsCount struct {
	Address     string `json:"address"`
	EventsCount string `json:"events_count"`
}

func (h handler) GetCsEvents(c *gin.Context) {
	var eventsCount []CsEventsCount
	if h.DB.Raw(`select oc.address as address, count(ec.id) as events_count from obj_consumers oc
    join public.event_consumers ec on oc.id = ec.obj_consumer_id
group by oc.address order by count(ec.id) desc`).Scan(&eventsCount).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "not found")
		return
	}
	c.JSON(http.StatusOK, &eventsCount)
}
