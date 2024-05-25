package models

import (
	"encoding/json"
	"time"
)

type ModelInfo struct {
	ID                uint64            `gorm:"primaryKey" json:"id"`
	Name              string            `gorm:"unique" json:"name"`
	Metrics           string            `json:"metrics"`
	Accuracy          float64           `json:"accuracy"`
	FeatureImportance FeatureImportance `gorm:"type:jsonb;default:'{}';" json:"feature_importance"`
	Created           time.Time         `gorm:"autoUpdateTime" json:"created"`
}

type FeatureImportance struct {
	Name       string  `json:"name"`
	Importance float64 `json:"importance"`
}

func (s *FeatureImportance) Scan(v interface{}) error {
	err := json.Unmarshal(v.([]byte), &s)
	if err != nil {
		return err
	}
	return nil
}
