package models

import "time"

type EventConsumer struct {
	ID            uint64         `gorm:"primaryKey" json:"id"`
	ObjConsumerId uint64         `json:"obj_consumer_id"`
	Source        string         `json:"source"` // additional source model
	Description   string         `json:"description"`
	IsApproved    bool           `gorm:"default:true;" json:"is_approved"`
	IsClosed      bool           `gorm:"default:true;" json:"is_closed"`
	Probability   float32        `gorm:"default:100.0;" json:"probability"`
	DaysOfWork    float64        `json:"days_of_work"`
	EventsCounter []EventCounter `json:"events_counter"`
	Created       time.Time      `gorm:"autoUpdateTime" json:"created"`
	Closed        time.Time      `json:"closed"`
}

type EventType struct {
	ID        uint64 `gorm:"primaryKey" json:"id"`
	EventName string `gorm:"unique" json:"event_name"`
}

type EventCounter struct {
	ID                uint64    `gorm:"primaryKey" json:"id"`
	ObjConsumerId     uint64    `json:"obj_consumer_id"`
	EventConsumerId   uint64    `json:"event_consumer_id"`
	Contour           string    `json:"contour"`
	CounterMark       string    `json:"counter_mark"`
	CounterNumber     int64     `json:"counter_number"`
	Created           time.Time `json:"created"`
	GcalInSystem      float64   `json:"gcal_in_system"`
	GcalOutSystem     float64   `json:"gcal_out_system"`
	Subset            float64   `json:"subset"`
	Leak              float64   `json:"leak"`
	SupplyTemp        float64   `json:"supply_temp"`
	ReturnTemp        float64   `json:"return_temp"`
	WorkHoursCounter  float64   `json:"work_hours_counter"`
	HeatThermalEnergy float64   `json:"heat_thermal_energy"`
	Errors            string    `json:"errors"`
	ErrorsDesc        string    `json:"errors_desc"`
}
