package models

import (
	"encoding/json"
	"time"
)

type ModelInfo struct {
	ID                uint64     `gorm:"primaryKey" json:"id"`
	Name              string     `gorm:"unique" json:"name"`
	Metrics           string     `json:"metrics"`
	Path              string     `json:"path"`
	Accuracy          float64    `json:"accuracy"`
	FeatureImportance FeatureImp `gorm:"type:jsonb;default:'{}';" json:"feature_importance"`
	Created           time.Time  `gorm:"autoUpdateTime" json:"created"`
}

type FeatureImp struct {
	FeatureImportances []FeatureImportance `json:"feature_importances"`
}

type FeatureImportance struct {
	Name  string  `json:"name"`
	Score float64 `json:"score"`
}

func (s *FeatureImp) Scan(v interface{}) error {
	err := json.Unmarshal(v.([]byte), &s)
	if err != nil {
		return err
	}
	return nil
}
