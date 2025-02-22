package weather

import (
	"encoding/json"
	"fmt"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"services01/pkg/models"
	"strconv"
	"strings"
	"time"
)

func getWeather(apiKey string, lat, lon float64) (*models.WeatherArea, error) {
	baseURL := "https://api.weather.yandex.ru/v2/forecast"
	client := &http.Client{}

	req, err := http.NewRequest("GET", baseURL, nil)
	if err != nil {
		return nil, err
	}

	// Установка заголовков
	req.Header.Add("X-Yandex-API-Key", apiKey)

	// Параметры запроса
	q := url.Values{}
	q.Add("lat", fmt.Sprintf("%f", lat))
	q.Add("lon", fmt.Sprintf("%f", lon))
	q.Add("limit", "5")
	q.Add("lang", "ru_RU")

	req.URL.RawQuery = q.Encode()

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer func(Body io.ReadCloser) {
		err := Body.Close()
		if err != nil {

		}
	}(resp.Body)
	fmt.Println(resp.StatusCode)
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var weather models.WeatherArea
	err = json.Unmarshal(body, &weather.TempInfo)
	if err != nil {
		return nil, err
	}

	return &weather, nil
}

func UpdateTempDataArea(db *gorm.DB) error {

	var areas []models.LocationArea

	err := db.Find(&areas).Error

	if err != nil {
		log.Println(err)
		return err
	}

	apiKey := os.Getenv("YA_WEATHER_KEY")
	for _, area := range areas {
		coordinates := strings.Split(area.Coordinates, " ")
		lat, err := strconv.ParseFloat(coordinates[0], 64)
		lon, err := strconv.ParseFloat(coordinates[1], 64)
		if err != nil {
			log.Println(err)
			return err
			//continue
		}
		weather, err := getWeather(apiKey, lat, lon)
		if err != nil {
			log.Println("Error retrieving weather:", err)
			return err
		}
		area.Weather = append(area.Weather, *weather)
		err = db.Save(&area).Error
		if err != nil {
			log.Println(err)
			return err
		}
	}
	return nil
}

func CalculateFallTemp(db *gorm.DB) error {
	var wthConditions []models.WeatherCondition
	db.Find(&wthConditions)
	var areas []models.LocationArea
	err := db.
		//Preload("Weather", func(tx *gorm.DB) *gorm.DB {
		//	return tx.Last(&models.WeatherArea{})
		//}).
		//Preload("Consumers").Find(&areas).Error
		//Preload("Consumers.WeatherFall").
		Preload(clause.Associations).Find(&areas).Error
	var nAreas []models.LocationArea
	for _, area := range areas {
		q := "select * from public.weather_areas where location_area_id='" + strconv.FormatUint(uint64(area.ID), 10) + "'"
		err := db.Raw(q).Scan(&area.Weather).Error
		if err != nil {
			continue
		}
		nAreas = append(nAreas, area)
	}

	flag := false
	var nParams []NewtonParams
	for _, area := range nAreas {
		for _, forecast := range area.Weather[0].TempInfo.Forecasts {
			tNow := time.Now().Format("2006-01-02")
			tForecast := time.Unix(int64(forecast.DateTs), 0).Format("2006-01-02")
			if tNow == tForecast || flag {
				hNow := time.Now()
				for _, data := range forecast.Hours {
					hForecast := time.Unix(int64(data.HourTs), 0)
					if hNow.Hour() == hForecast.Hour() || flag {
						var condition float64
						for _, wthCondition := range wthConditions {
							if wthCondition.Name == data.Condition {
								condition = wthCondition.K
								break
							}
						}
						flag = true
						nParams = append(nParams, NewtonParams{
							K:             0.0,
							WindSpeed:     data.WindSpeed,
							Humidity:      float64(data.Humidity),
							TInitial:      0.0,
							TEnv:          float64(data.Temp),
							Weather:       condition,
							WindDirection: data.WindDir,
							DateTs:        int64(data.HourTs),
						})
					}
				}
			}

		}
		var consumers []models.ObjConsumer
		db.Where("location_area_id = ?", area.ID).Preload("WallMaterial").Find(&consumers)
		err = PredicateTemp(db, &consumers, &nParams, &wthConditions)
		if err != nil {
			return err
		}
	}
	return nil
}

func PredicateTemp(db *gorm.DB, consumers *[]models.ObjConsumer, weatherParams *[]NewtonParams, wthConditions *[]models.WeatherCondition) error {
	t := time.Now()
	nTime := time.Date(t.Year(), t.Month(), t.Day(), t.Hour(), 0, 0, 0, time.Local)
	startTime := nTime.Unix() - 3600

	for _, consumer := range *consumers {
		var fallWeather models.WeatherConsumerFall
		var tempData models.TempData
		tInitial := consumer.TempConditions.SummerHigh
		tempData.DateTs = startTime
		tempData.Temp = tInitial
		fallWeather.TempDropping.TempData = append(fallWeather.TempDropping.TempData, tempData)
		for _, wthr := range *weatherParams {
			if len(fallWeather.TempDropping.TempData) == 1 {
				if wthr.TEnv > tInitial {
					fallWeather.TempDropping.TempData[0].Temp = wthr.TEnv
				}
				fallWeather.TempDropping.TempData[0].EnvTemp = wthr.TEnv
			}
			tempData.DateTs = wthr.DateTs
			if len(consumer.WallMaterial) > 0 {
				wthr.K = consumer.WallMaterial[0].K
			} else {
				wthr.K = 0.01
			}
			wthr.TInitial = tInitial
			tInitial = NewtonCooling(&wthr)
			tempData.Temp = tInitial
			tempData.EnvTemp = wthr.TEnv
			fallWeather.TempDropping.TempData = append(fallWeather.TempDropping.TempData, tempData)
			if tInitial <= 18 {
				break
			}
		}
		consumer.WeatherFall = append(consumer.WeatherFall, fallWeather)
		err := db.Save(&consumer).Error
		if err != nil {
			log.Println(err)
			return err
		}
	}
	return nil
}
