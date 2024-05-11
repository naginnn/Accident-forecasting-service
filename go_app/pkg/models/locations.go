package models

type LocationDistrict struct {
	ID        uint           `json:"id"`
	Name      string         `gorm:"unique" json:"name"`
	ShortName string         `json:"short_name"`
	Areas     []LocationArea `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"consumers"`
}

type LocationArea struct {
	ID                 uint          `json:"id"`
	LocationDistrictId uint          `json:"location_district_id"`
	Name               string        `gorm:"unique" json:"name"`
	Coordinates        string        `json:"coordinates"`
	Weather            []WeatherArea `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"weather"`
	Consumers          []ObjConsumer `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"consumers"`
}
