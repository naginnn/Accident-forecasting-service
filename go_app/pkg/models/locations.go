package models

import (
	"encoding/json"
	"time"
)

type ObjDistrict struct {
	ID        uint      `json:"id"`
	Name      string    `gorm:"unique" json:"name"`
	ShortName string    `json:"short_name"`
	Areas     []ObjArea `gorm:"constraint:OnUpdate:CASCADE,OnDelete:SET NULL;" json:"consumers"`
}

type ObjArea struct {
	ID                 uint      `json:"id"`
	ObjDistrictId      uint      `json:"obj_district_id"`
	Name               string    `gorm:"unique" json:"name"`
	Coordinates        string    `json:"coordinates"`
	TempData           TempData  `gorm:"type:jsonb;default:'{}';" json:"temp_data"`
	LastUpdateTempData time.Time `gorm:"autoUpdateTime" json:"last_update_temp_data"`
}

type T struct {
	Date      string `json:"date"`
	DateTs    int    `json:"date_ts"`
	Week      int    `json:"week"`
	Sunrise   string `json:"sunrise"`
	Sunset    string `json:"sunset"`
	RiseBegin string `json:"rise_begin"`
	SetEnd    string `json:"set_end"`
	MoonCode  int    `json:"moon_code"`
	MoonText  string `json:"moon_text"`
	Parts     struct {
		Day struct {
			Source       string      `json:"_source"`
			TempMin      int         `json:"temp_min"`
			TempAvg      int         `json:"temp_avg"`
			TempMax      int         `json:"temp_max"`
			WindSpeed    float64     `json:"wind_speed"`
			WindGust     float64     `json:"wind_gust"`
			WindDir      string      `json:"wind_dir"`
			PressureMm   int         `json:"pressure_mm"`
			PressurePa   int         `json:"pressure_pa"`
			Humidity     int         `json:"humidity"`
			SoilTemp     int         `json:"soil_temp"`
			SoilMoisture float64     `json:"soil_moisture"`
			PrecMm       float64     `json:"prec_mm"`
			PrecProb     int         `json:"prec_prob"`
			PrecPeriod   int         `json:"prec_period"`
			Cloudness    float64     `json:"cloudness"`
			PrecType     int         `json:"prec_type"`
			PrecStrength float64     `json:"prec_strength"`
			Icon         string      `json:"icon"`
			Condition    string      `json:"condition"`
			UvIndex      int         `json:"uv_index,omitempty"`
			FeelsLike    int         `json:"feels_like"`
			Daytime      string      `json:"daytime"`
			Polar        interface{} `json:"polar"`
			FreshSnowMm  int         `json:"fresh_snow_mm"`
		} `json:"day"`
		DayShort struct {
			Source       string      `json:"_source"`
			Temp         int         `json:"temp"`
			TempMin      int         `json:"temp_min"`
			WindSpeed    float64     `json:"wind_speed"`
			WindGust     float64     `json:"wind_gust"`
			WindDir      string      `json:"wind_dir"`
			PressureMm   int         `json:"pressure_mm"`
			PressurePa   int         `json:"pressure_pa"`
			Humidity     int         `json:"humidity"`
			SoilTemp     int         `json:"soil_temp"`
			SoilMoisture float64     `json:"soil_moisture"`
			PrecMm       float64     `json:"prec_mm"`
			PrecProb     int         `json:"prec_prob"`
			PrecPeriod   int         `json:"prec_period"`
			Cloudness    float64     `json:"cloudness"`
			PrecType     int         `json:"prec_type"`
			PrecStrength float64     `json:"prec_strength"`
			Icon         string      `json:"icon"`
			Condition    string      `json:"condition"`
			UvIndex      int         `json:"uv_index,omitempty"`
			FeelsLike    int         `json:"feels_like"`
			Daytime      string      `json:"daytime"`
			Polar        interface{} `json:"polar"`
			FreshSnowMm  int         `json:"fresh_snow_mm"`
		} `json:"day_short"`
		Evening struct {
			Source       string      `json:"_source"`
			TempMin      int         `json:"temp_min"`
			TempAvg      int         `json:"temp_avg"`
			TempMax      int         `json:"temp_max"`
			WindSpeed    float64     `json:"wind_speed"`
			WindGust     float64     `json:"wind_gust"`
			WindDir      string      `json:"wind_dir"`
			PressureMm   int         `json:"pressure_mm"`
			PressurePa   int         `json:"pressure_pa"`
			Humidity     int         `json:"humidity"`
			SoilTemp     int         `json:"soil_temp"`
			SoilMoisture float64     `json:"soil_moisture"`
			PrecMm       float64     `json:"prec_mm"`
			PrecProb     int         `json:"prec_prob"`
			PrecPeriod   int         `json:"prec_period"`
			Cloudness    float64     `json:"cloudness"`
			PrecType     int         `json:"prec_type"`
			PrecStrength float64     `json:"prec_strength"`
			Icon         string      `json:"icon"`
			Condition    string      `json:"condition"`
			UvIndex      int         `json:"uv_index,omitempty"`
			FeelsLike    int         `json:"feels_like"`
			Daytime      string      `json:"daytime"`
			Polar        interface{} `json:"polar"`
			FreshSnowMm  int         `json:"fresh_snow_mm"`
		} `json:"evening"`
		Morning struct {
			Source       string      `json:"_source"`
			TempMin      int         `json:"temp_min"`
			TempAvg      int         `json:"temp_avg"`
			TempMax      int         `json:"temp_max"`
			WindSpeed    float64     `json:"wind_speed"`
			WindGust     float64     `json:"wind_gust"`
			WindDir      string      `json:"wind_dir"`
			PressureMm   int         `json:"pressure_mm"`
			PressurePa   int         `json:"pressure_pa"`
			Humidity     int         `json:"humidity"`
			SoilTemp     int         `json:"soil_temp"`
			SoilMoisture float64     `json:"soil_moisture"`
			PrecMm       float64     `json:"prec_mm"`
			PrecProb     int         `json:"prec_prob"`
			PrecPeriod   int         `json:"prec_period"`
			Cloudness    float64     `json:"cloudness"`
			PrecType     int         `json:"prec_type"`
			PrecStrength float64     `json:"prec_strength"`
			Icon         string      `json:"icon"`
			Condition    string      `json:"condition"`
			UvIndex      int         `json:"uv_index,omitempty"`
			FeelsLike    int         `json:"feels_like"`
			Daytime      string      `json:"daytime"`
			Polar        interface{} `json:"polar"`
			FreshSnowMm  int         `json:"fresh_snow_mm"`
		} `json:"morning"`
		Night struct {
			Source       string      `json:"_source"`
			TempMin      int         `json:"temp_min"`
			TempAvg      int         `json:"temp_avg"`
			TempMax      int         `json:"temp_max"`
			WindSpeed    float64     `json:"wind_speed"`
			WindGust     float64     `json:"wind_gust"`
			WindDir      string      `json:"wind_dir"`
			PressureMm   int         `json:"pressure_mm"`
			PressurePa   int         `json:"pressure_pa"`
			Humidity     int         `json:"humidity"`
			SoilTemp     int         `json:"soil_temp"`
			SoilMoisture float64     `json:"soil_moisture"`
			PrecMm       float64     `json:"prec_mm"`
			PrecProb     int         `json:"prec_prob"`
			PrecPeriod   int         `json:"prec_period"`
			Cloudness    float64     `json:"cloudness"`
			PrecType     int         `json:"prec_type"`
			PrecStrength float64     `json:"prec_strength"`
			Icon         string      `json:"icon"`
			Condition    string      `json:"condition"`
			UvIndex      int         `json:"uv_index,omitempty"`
			FeelsLike    int         `json:"feels_like"`
			Daytime      string      `json:"daytime"`
			Polar        interface{} `json:"polar"`
			FreshSnowMm  int         `json:"fresh_snow_mm"`
		} `json:"night"`
		NightShort struct {
			Source       string      `json:"_source"`
			Temp         int         `json:"temp"`
			WindSpeed    float64     `json:"wind_speed"`
			WindGust     float64     `json:"wind_gust"`
			WindDir      string      `json:"wind_dir"`
			PressureMm   int         `json:"pressure_mm"`
			PressurePa   int         `json:"pressure_pa"`
			Humidity     int         `json:"humidity"`
			SoilTemp     int         `json:"soil_temp"`
			SoilMoisture float64     `json:"soil_moisture"`
			PrecMm       float64     `json:"prec_mm"`
			PrecProb     int         `json:"prec_prob"`
			PrecPeriod   int         `json:"prec_period"`
			Cloudness    float64     `json:"cloudness"`
			PrecType     int         `json:"prec_type"`
			PrecStrength float64     `json:"prec_strength"`
			Icon         string      `json:"icon"`
			Condition    string      `json:"condition"`
			UvIndex      int         `json:"uv_index,omitempty"`
			FeelsLike    int         `json:"feels_like"`
			Daytime      string      `json:"daytime"`
			Polar        interface{} `json:"polar"`
			FreshSnowMm  int         `json:"fresh_snow_mm"`
		} `json:"night_short"`
	} `json:"parts"`
	Hours []struct {
		Hour         string      `json:"hour"`
		HourTs       int         `json:"hour_ts"`
		Temp         int         `json:"temp"`
		FeelsLike    int         `json:"feels_like"`
		Icon         string      `json:"icon"`
		Condition    string      `json:"condition"`
		Cloudness    float64     `json:"cloudness"`
		PrecType     int         `json:"prec_type"`
		PrecStrength float64     `json:"prec_strength"`
		IsThunder    interface{} `json:"is_thunder"`
		WindDir      string      `json:"wind_dir"`
		WindSpeed    float64     `json:"wind_speed"`
		WindGust     float64     `json:"wind_gust"`
		PressureMm   int         `json:"pressure_mm"`
		PressurePa   int         `json:"pressure_pa"`
		Humidity     int         `json:"humidity"`
		UvIndex      int         `json:"uv_index"`
		SoilTemp     int         `json:"soil_temp"`
		SoilMoisture float64     `json:"soil_moisture"`
		PrecMm       float64     `json:"prec_mm"`
		PrecPeriod   int         `json:"prec_period"`
		PrecProb     int         `json:"prec_prob"`
	} `json:"hours"`
	Biomet struct {
		Index     int    `json:"index"`
		Condition string `json:"condition"`
	} `json:"biomet,omitempty"`
}

type TempData struct {
	Forecasts []struct {
		Date      string `json:"date"`
		DateTs    int    `json:"date_ts"`
		Week      int    `json:"week"`
		Sunrise   string `json:"sunrise"`
		Sunset    string `json:"sunset"`
		RiseBegin string `json:"rise_begin"`
		SetEnd    string `json:"set_end"`
		MoonCode  int    `json:"moon_code"`
		MoonText  string `json:"moon_text"`
		Parts     struct {
			Day struct {
				Source       string      `json:"_source"`
				TempMin      int         `json:"temp_min"`
				TempAvg      int         `json:"temp_avg"`
				TempMax      int         `json:"temp_max"`
				WindSpeed    float64     `json:"wind_speed"`
				WindGust     float64     `json:"wind_gust"`
				WindDir      string      `json:"wind_dir"`
				PressureMm   int         `json:"pressure_mm"`
				PressurePa   int         `json:"pressure_pa"`
				Humidity     int         `json:"humidity"`
				SoilTemp     int         `json:"soil_temp"`
				SoilMoisture float64     `json:"soil_moisture"`
				PrecMm       float64     `json:"prec_mm"`
				PrecProb     int         `json:"prec_prob"`
				PrecPeriod   int         `json:"prec_period"`
				Cloudness    float64     `json:"cloudness"`
				PrecType     int         `json:"prec_type"`
				PrecStrength float64     `json:"prec_strength"`
				Icon         string      `json:"icon"`
				Condition    string      `json:"condition"`
				UvIndex      int         `json:"uv_index,omitempty"`
				FeelsLike    int         `json:"feels_like"`
				Daytime      string      `json:"daytime"`
				Polar        interface{} `json:"polar"`
				FreshSnowMm  int         `json:"fresh_snow_mm"`
			} `json:"day"`
			DayShort struct {
				Source       string      `json:"_source"`
				Temp         int         `json:"temp"`
				TempMin      int         `json:"temp_min"`
				WindSpeed    float64     `json:"wind_speed"`
				WindGust     float64     `json:"wind_gust"`
				WindDir      string      `json:"wind_dir"`
				PressureMm   int         `json:"pressure_mm"`
				PressurePa   int         `json:"pressure_pa"`
				Humidity     int         `json:"humidity"`
				SoilTemp     int         `json:"soil_temp"`
				SoilMoisture float64     `json:"soil_moisture"`
				PrecMm       float64     `json:"prec_mm"`
				PrecProb     int         `json:"prec_prob"`
				PrecPeriod   int         `json:"prec_period"`
				Cloudness    float64     `json:"cloudness"`
				PrecType     int         `json:"prec_type"`
				PrecStrength float64     `json:"prec_strength"`
				Icon         string      `json:"icon"`
				Condition    string      `json:"condition"`
				UvIndex      int         `json:"uv_index,omitempty"`
				FeelsLike    int         `json:"feels_like"`
				Daytime      string      `json:"daytime"`
				Polar        interface{} `json:"polar"`
				FreshSnowMm  int         `json:"fresh_snow_mm"`
			} `json:"day_short"`
			Evening struct {
				Source       string      `json:"_source"`
				TempMin      int         `json:"temp_min"`
				TempAvg      int         `json:"temp_avg"`
				TempMax      int         `json:"temp_max"`
				WindSpeed    float64     `json:"wind_speed"`
				WindGust     float64     `json:"wind_gust"`
				WindDir      string      `json:"wind_dir"`
				PressureMm   int         `json:"pressure_mm"`
				PressurePa   int         `json:"pressure_pa"`
				Humidity     int         `json:"humidity"`
				SoilTemp     int         `json:"soil_temp"`
				SoilMoisture float64     `json:"soil_moisture"`
				PrecMm       float64     `json:"prec_mm"`
				PrecProb     int         `json:"prec_prob"`
				PrecPeriod   int         `json:"prec_period"`
				Cloudness    float64     `json:"cloudness"`
				PrecType     int         `json:"prec_type"`
				PrecStrength float64     `json:"prec_strength"`
				Icon         string      `json:"icon"`
				Condition    string      `json:"condition"`
				UvIndex      int         `json:"uv_index,omitempty"`
				FeelsLike    int         `json:"feels_like"`
				Daytime      string      `json:"daytime"`
				Polar        interface{} `json:"polar"`
				FreshSnowMm  int         `json:"fresh_snow_mm"`
			} `json:"evening"`
			Morning struct {
				Source       string      `json:"_source"`
				TempMin      int         `json:"temp_min"`
				TempAvg      int         `json:"temp_avg"`
				TempMax      int         `json:"temp_max"`
				WindSpeed    float64     `json:"wind_speed"`
				WindGust     float64     `json:"wind_gust"`
				WindDir      string      `json:"wind_dir"`
				PressureMm   int         `json:"pressure_mm"`
				PressurePa   int         `json:"pressure_pa"`
				Humidity     int         `json:"humidity"`
				SoilTemp     int         `json:"soil_temp"`
				SoilMoisture float64     `json:"soil_moisture"`
				PrecMm       float64     `json:"prec_mm"`
				PrecProb     int         `json:"prec_prob"`
				PrecPeriod   int         `json:"prec_period"`
				Cloudness    float64     `json:"cloudness"`
				PrecType     int         `json:"prec_type"`
				PrecStrength float64     `json:"prec_strength"`
				Icon         string      `json:"icon"`
				Condition    string      `json:"condition"`
				UvIndex      int         `json:"uv_index,omitempty"`
				FeelsLike    int         `json:"feels_like"`
				Daytime      string      `json:"daytime"`
				Polar        interface{} `json:"polar"`
				FreshSnowMm  int         `json:"fresh_snow_mm"`
			} `json:"morning"`
			Night struct {
				Source       string      `json:"_source"`
				TempMin      int         `json:"temp_min"`
				TempAvg      int         `json:"temp_avg"`
				TempMax      int         `json:"temp_max"`
				WindSpeed    float64     `json:"wind_speed"`
				WindGust     float64     `json:"wind_gust"`
				WindDir      string      `json:"wind_dir"`
				PressureMm   int         `json:"pressure_mm"`
				PressurePa   int         `json:"pressure_pa"`
				Humidity     int         `json:"humidity"`
				SoilTemp     int         `json:"soil_temp"`
				SoilMoisture float64     `json:"soil_moisture"`
				PrecMm       float64     `json:"prec_mm"`
				PrecProb     int         `json:"prec_prob"`
				PrecPeriod   int         `json:"prec_period"`
				Cloudness    float64     `json:"cloudness"`
				PrecType     int         `json:"prec_type"`
				PrecStrength float64     `json:"prec_strength"`
				Icon         string      `json:"icon"`
				Condition    string      `json:"condition"`
				UvIndex      int         `json:"uv_index,omitempty"`
				FeelsLike    int         `json:"feels_like"`
				Daytime      string      `json:"daytime"`
				Polar        interface{} `json:"polar"`
				FreshSnowMm  int         `json:"fresh_snow_mm"`
			} `json:"night"`
			NightShort struct {
				Source       string      `json:"_source"`
				Temp         int         `json:"temp"`
				WindSpeed    float64     `json:"wind_speed"`
				WindGust     float64     `json:"wind_gust"`
				WindDir      string      `json:"wind_dir"`
				PressureMm   int         `json:"pressure_mm"`
				PressurePa   int         `json:"pressure_pa"`
				Humidity     int         `json:"humidity"`
				SoilTemp     int         `json:"soil_temp"`
				SoilMoisture float64     `json:"soil_moisture"`
				PrecMm       float64     `json:"prec_mm"`
				PrecProb     int         `json:"prec_prob"`
				PrecPeriod   int         `json:"prec_period"`
				Cloudness    float64     `json:"cloudness"`
				PrecType     int         `json:"prec_type"`
				PrecStrength float64     `json:"prec_strength"`
				Icon         string      `json:"icon"`
				Condition    string      `json:"condition"`
				UvIndex      int         `json:"uv_index,omitempty"`
				FeelsLike    int         `json:"feels_like"`
				Daytime      string      `json:"daytime"`
				Polar        interface{} `json:"polar"`
				FreshSnowMm  int         `json:"fresh_snow_mm"`
			} `json:"night_short"`
		} `json:"parts"`
		Hours []struct {
			Hour         string      `json:"hour"`
			HourTs       int         `json:"hour_ts"`
			Temp         int         `json:"temp"`
			FeelsLike    int         `json:"feels_like"`
			Icon         string      `json:"icon"`
			Condition    string      `json:"condition"`
			Cloudness    float64     `json:"cloudness"`
			PrecType     int         `json:"prec_type"`
			PrecStrength float64     `json:"prec_strength"`
			IsThunder    interface{} `json:"is_thunder"`
			WindDir      string      `json:"wind_dir"`
			WindSpeed    float64     `json:"wind_speed"`
			WindGust     float64     `json:"wind_gust"`
			PressureMm   int         `json:"pressure_mm"`
			PressurePa   int         `json:"pressure_pa"`
			Humidity     int         `json:"humidity"`
			UvIndex      int         `json:"uv_index"`
			SoilTemp     int         `json:"soil_temp"`
			SoilMoisture float64     `json:"soil_moisture"`
			PrecMm       float64     `json:"prec_mm"`
			PrecPeriod   int         `json:"prec_period"`
			PrecProb     int         `json:"prec_prob"`
		} `json:"hours"`
		Biomet struct {
			Index     int    `json:"index"`
			Condition string `json:"condition"`
		} `json:"biomet,omitempty"`
	} `json:"forecasts"`
}

func (s *TempData) Scan(v interface{}) error {
	err := json.Unmarshal(v.([]byte), &s)
	if err != nil {
		return err
	}
	return nil
}
