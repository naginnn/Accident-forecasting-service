package models

import "time"

type ObjConsumerStation struct {
	ID            uint64             `gorm:"primaryKey" json:"id"`
	ObjDistrictId uint64             `json:"obj_district_id"`
	ObjAreaId     uint64             `json:"obj_area_id"`
	Name          string             `json:"name"`
	Address       string             `json:"address"`
	Coordinates   string             `json:"coordinates"`
	SourceStation []ObjSourceStation `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"source_station"`
	Consumers     []ObjConsumer      `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"consumers"`
}

type ObjSourceStation struct {
	ID                   uint64 `gorm:"primaryKey" json:"id"`
	ObjConsumerStationId uint64 `json:"obj_consumer_station_id"`
	ObjDistrictId        uint64 `json:"obj_district_id"`
	ObjAreaId            uint64 `json:"obj_area_id"`
	Name                 string `json:"name"`
	Address              string `json:"address"`
	Coordinates          string `json:"coordinates"`
}

/*
1. Критичный
2. Средний
3. Наименьшая критичность

Type: Тип
	1 Social
	2 Industrial
	3 MKD
EnergyClass: Класс энергоэффективности
	1. С and down
	2. В
	3. А and down
OperatingMode: Время работы
	1. Around the clock
	2. 9:00 - 21:00
	3. 9:00 – 18:00
*/

type ObjConsumer struct {
	ID                   uint64  `gorm:"primaryKey" json:"id"`
	ObjConsumerStationId uint64  `json:"obj_consumer_station_id"`
	ObjDistrictId        uint64  `json:"obj_district_id"`
	ObjAreaId            uint64  `json:"obj_area_id"`
	Name                 string  `json:"name"`
	Address              string  `json:"address"`
	Coordinates          string  `json:"coordinates"`
	WallMaterial         string  `json:"wall_material"`
	RoofMaterial         string  `json:"roof_material"`
	TotalArea            float64 `json:"total_area"`
	LivingArea           float64 `json:"living_area"`
	NotLivingArea        float64 `json:"not_living_area"`
	// Temperature
	FactTemp    float64 `json:"fact_temp"`
	OutsideTemp float64 `json:"outside_temp"`
	// critical parameters
	Type          string `json:"type"`
	EnergyClass   string `json:"energy_class"`
	OperatingMode string `json:"operating_mode"`
}

type ObjConsumerEvent struct {
	ID            uint64    `gorm:"primaryKey" json:"id"`
	ObjConsumerId uint64    `json:"obj_consumer_id"` // foreign key Consumer
	Source        string    `json:"source"`
	System        string    `json:"system"`
	Name          string    `json:"name"`
	Description   string    `json:"description"`
	Created       time.Time `json:"created"`
	Closed        time.Time `json:"closed"`
}
