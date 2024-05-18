package models

import "time"

type PredictionAccident struct {
	ID                   uint64    `gorm:"primaryKey" json:"id"`
	ObjConsumerStationId uint64    `json:"obj_consumer_station_id"`
	ObjConsumerId        uint64    `json:"obj_consumer_id"`
	IsAccident           bool      `json:"is_accident"`
	Percent              float64   `json:"percent"`
	IsApproved           bool      `json:"is_approved"`
	IsActual             bool      `json:"is_actual"`
	IsClosed             bool      `json:"is_closed"`
	Created              time.Time `json:"created"`
	Closed               time.Time `json:"closed"`
}
