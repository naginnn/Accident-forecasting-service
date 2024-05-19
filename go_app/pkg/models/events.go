package models

import "time"

type EventConsumer struct {
	ID            uint64    `gorm:"primaryKey" json:"id"`
	ObjConsumerId uint64    `json:"obj_consumer_id"`
	Source        string    `json:"source"` // additional source model
	Description   string    `json:"description"`
	IsApproved    bool      `gorm:"default:true;" json:"is_approved"`
	IsClosed      bool      `gorm:"default:true;" json:"is_closed"`
	Probability   float32   `gorm:"default:100.0;" json:"probability"`
	DaysOfWork    float64   `json:"days_of_work"`
	Created       time.Time `gorm:"autoUpdateTime" json:"created"`
	Closed        time.Time `json:"closed"`
}

type EventType struct {
	ID        uint64 `gorm:"primaryKey" json:"id"`
	EventName string `gorm:"unique" json:"event_name"`
}
