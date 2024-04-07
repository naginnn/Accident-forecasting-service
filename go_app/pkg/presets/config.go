package presets

import (
	"gorm.io/gorm"
	"services01/pkg/db"
)

type Config struct {
	DB *gorm.DB
}

func GetConfig(appName string) (*Config, error) {
	DB, err := db.Init(appName)
	if err != nil {
		return nil, err
	}
	return &Config{DB: DB}, nil
}
