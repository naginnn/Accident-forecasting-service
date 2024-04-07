package models

type UsrData struct {
	ID    uint   `json:"id"`
	Name  string `gorm:"unique" json:"name"`
	Pwd   string `json:"pwd"`
	Roles string `json:"roles"`
}
