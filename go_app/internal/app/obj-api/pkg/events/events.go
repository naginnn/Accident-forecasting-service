package events

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/models"
	"time"
)

func (h handler) GetEvents(c *gin.Context) {
	var events []models.EventConsumer
	if h.DB.Find(&events).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "Events not found")
		return
	}
	c.JSON(http.StatusOK, &events)
}

func (h handler) GetEvent(c *gin.Context) {
	id := c.Param("id")
	var event models.EventConsumer
	if h.DB.Select("*").
		Where("id = ?", id).Find(&event).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "Event not found")
		return
	}

	c.JSON(http.StatusOK, &event)
}

func (h handler) UpdateEvent(c *gin.Context) {
	id := c.Query("id")
	var event models.EventConsumer
	if h.DB.Where("id = ?", id).Find(&event).RowsAffected == 0 {
		c.JSON(http.StatusNotFound, "Event not found")
		return
	}
	cmd := c.Query("cmd")

	switch cmd {
	case "approve":
		event.IsApproved = true
		event.Probability = 100
		h.DB.Model(&event).Save(event)
	case "close":
		currentTime := time.Now()
		repairDays := (currentTime.Unix() - event.Created.Unix()) / 86400
		event.Closed = currentTime
		event.IsClosed = true
		event.DaysOfWork = float64(repairDays)
		h.DB.Model(&event).Save(event)
	case "cancel":
		h.DB.Model(&event).Delete(event)
	default:
		c.JSON(http.StatusNotFound, "Event not found")
		return
	}
	c.JSON(http.StatusOK, &event)
}
