package models

type MaterialWall struct {
	ID        uint64         `gorm:"primaryKey" json:"id"`
	Consumers []*ObjConsumer `gorm:"many2many:material_consumer_walls" json:"consumers"`
	Name      string         `gorm:"unique" json:"name"`
	K         float64        `json:"k"`
}
