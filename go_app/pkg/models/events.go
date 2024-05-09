package models

import "time"

type EventConsumer struct {
	ID            uint64    `gorm:"primaryKey" json:"id"`
	ObjConsumerId uint64    `json:"obj_consumer_id"`
	Source        string    `json:"source"`
	System        string    `json:"system"`
	Name          string    `json:"name"`
	Description   string    `json:"description"`
	Created       time.Time `gorm:"autoUpdateTime" json:"created"`
	Closed        time.Time `json:"closed"`
}
