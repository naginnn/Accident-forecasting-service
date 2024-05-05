package models

import "time"

type ObjDistrict struct {
	ID        uint      `json:"id"`
	Name      string    `gorm:"unique" json:"name"`
	ShortName string    `json:"short_name"`
	Areas     []ObjArea `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"consumers"`
}

type ObjArea struct {
	ID             uint      `json:"id"`
	ObjDistrictId  uint      `json:"obj_district_id"`
	Name           string    `gorm:"unique" json:"name"`
	Coordinates    string    `json:"coordinates"`
	FactTemp       float64   `json:"fact_temp"`
	LastUpdateTemp time.Time `json:"last_update_temp"`
}
