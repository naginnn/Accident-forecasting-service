package models

type ObjConsumerStation struct {
	ID             uint64               `gorm:"primaryKey" json:"id"`
	ObjDistrictId  uint64               `json:"obj_district_id"`
	ObjAreaId      uint64               `json:"obj_area_id"`
	Name           string               `json:"name"`
	Address        string               `json:"address"`
	Coordinates    string               `json:"coordinates"`
	SourceStations []*ObjSourceStation  `gorm:"many2many:obj_source_consumer_stations" json:"source_stations"`
	Consumers      []ObjConsumer        `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"consumers"`
	Accidents      []PredictionAccident `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"accidents"`
}

type ObjSourceStation struct {
	ID               uint64                `gorm:"primaryKey" json:"id"`
	ObjDistrictId    uint64                `json:"obj_district_id"`
	ObjAreaId        uint64                `json:"obj_area_id"`
	Name             string                `json:"name"`
	Address          string                `json:"address"`
	Coordinates      string                `json:"coordinates"`
	ConsumerStations []*ObjConsumerStation `gorm:"many2many:obj_source_consumer_stations" json:"consumer_stations"`
}

type ObjConsumer struct {
	ID                   uint64  `gorm:"primaryKey" json:"id"`
	ObjConsumerStationId uint64  `json:"obj_consumer_station_id"`
	ObjDistrictId        uint64  `json:"obj_district_id"`
	ObjAreaId            uint64  `json:"obj_area_id"`
	Name                 string  `json:"name"`
	Address              string  `json:"address"`
	Coordinates          string  `json:"coordinates"`
	TotalArea            float64 `json:"total_area"`
	LivingArea           float64 `json:"living_area"`
	NotLivingArea        float64 `json:"not_living_area"`
	Type                 string  `json:"type"`
	EnergyClass          string  `json:"energy_class"`
	OperatingMode        string  `json:"operating_mode"`
	Priority             int64   `json:"priority"`

	Accidents    []PredictionAccident  `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"accidents"`
	WeatherFall  []WeatherConsumerFall `json:"weather_fall"`
	Events       []EventConsumer       `json:"events"`
	WallMaterial []*MaterialWall       `gorm:"many2many:material_consumer_walls" json:"wall_material"`
	RoofMaterial []*MaterialRoof       `gorm:"many2many:material_consumer_roofs" json:"roof_material"`
}
