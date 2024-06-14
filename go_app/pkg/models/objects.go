package models

import (
	"encoding/json"
	"time"
)

type ObjConsumerStation struct {
	ID                 uint64              `gorm:"primaryKey" json:"id"`
	LocationDistrictId uint64              `json:"location_district_id"`
	LocationAreaId     uint64              `json:"location_area_id"`
	Name               string              `gorm:"unique" json:"name"`
	Address            string              `json:"address"`
	GeoData            GeoData             `gorm:"type:jsonb;default:'{}';" json:"geo_data"`
	Type               string              `json:"type"`
	PlaceType          string              `json:"place_type"`
	OdsName            string              `json:"ods_name"`
	OdsAddress         string              `json:"ods_address"`
	OdsIdUU            string              `json:"ods_id_uu"`
	OdsManagerCompany  string              `json:"ods_manager_company"`
	SourceStations     []*ObjSourceStation `gorm:"many2many:obj_source_consumer_stations" json:"source_stations"`
	Consumers          []ObjConsumer       `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"consumers"`
}

type ObjSourceStation struct {
	ID                 uint64                `gorm:"primaryKey" json:"id"`
	LocationDistrictId uint64                `json:"location_district_id"`
	LocationAreaId     uint64                `json:"location_area_id"`
	Name               string                `gorm:"unique" json:"name"`
	Address            string                `json:"address"`
	EPower             int64                 `json:"e_power"`
	TPower             int64                 `json:"t_power"`
	BoilerCount        int64                 `json:"boiler_count"`
	TurbineCount       int64                 `json:"turbine_count"`
	LaunchedDate       time.Time             `json:"launched_date"`
	GeoData            GeoData               `gorm:"type:jsonb;default:'{}';" json:"geo_data"`
	ConsumerStations   []*ObjConsumerStation `gorm:"many2many:obj_source_consumer_stations" json:"consumer_stations"`
}

type ObjConsumer struct {
	ID                   uint64 `gorm:"primaryKey" json:"id"`
	ObjConsumerStationId uint64 `json:"obj_consumer_station_id"`
	LocationDistrictId   uint64 `json:"location_district_id"`
	LocationAreaId       uint64 `json:"location_area_id"`

	Address      string `gorm:"unique" json:"address"`
	Street       string `json:"street"`
	HouseType    string `json:"house_type"`
	HouseNumber  string `json:"house_number"`
	CorpusNumber string `json:"corpus_number"`
	SoorType     string `json:"soor_type"`
	SoorNumber   string `json:"soor_number"`

	BalanceHolder string `json:"balance_holder"`
	LoadGvs       string `json:"load_gvs"`
	LoadFact      string `json:"load_fact"`
	HeatLoad      string `json:"heat_load"`
	VentLoad      string `json:"vent_load"`

	GeoData   GeoData `gorm:"type:jsonb;default:'{}';" json:"geo_data"`
	TotalArea float64 `json:"total_area"`
	Target    string  `json:"target"`
	BClass    string  `json:"b_class"`
	Floors    int64   `json:"floors"`
	Number    string  `json:"number"`
	WearPct   string  `json:"wear_pct"`
	BuildYear int64   `json:"build_year"`

	Type          string `json:"type"`
	SockType      string `json:"sock_type"`
	EnergyClass   string `json:"energy_class"`
	OperatingMode string `json:"operating_mode"`
	Priority      int64  `json:"priority"`

	IsDispatch bool `json:"is_dispatch"`

	TempConditions TempCondition         `gorm:"type:jsonb;default:'{}';" json:"temp_conditions"`
	WeatherFall    []WeatherConsumerFall `json:"weather_fall"`
	EventsCounter  []EventCounter        `json:"events_counter"`
	Events         []EventConsumer       `json:"events"`
	WallMaterial   []*MaterialWall       `gorm:"many2many:material_consumer_walls" json:"wall_material"`
}

type TempCondition struct {
	SummerHigh float64 `json:"summer_high"`
	SummerLow  float64 `json:"summer_low"`
	WinterHigh float64 `json:"winter_high"`
	WinterLow  float64 `json:"winter_low"`
}

func (s *TempCondition) Scan(v interface{}) error {
	err := json.Unmarshal(v.([]byte), &s)
	if err != nil {
		return err
	}
	return nil
}

type GeoData struct {
	Polygon [][]float64 `json:"polygon"`
	Center  []float64   `json:"center"`
}

func (s *GeoData) Scan(v interface{}) error {
	err := json.Unmarshal(v.([]byte), &s)
	if err != nil {
		return err
	}
	return nil
}
