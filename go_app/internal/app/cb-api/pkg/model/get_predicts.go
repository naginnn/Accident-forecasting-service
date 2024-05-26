package model

import (
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"os"
	"reflect"
	"services01/pkg/ml/wrapper/catboost"
	"slices"
)

type Predictable struct {
	SourceStationId      int `json:"source_station_id"`
	CsId                 int `json:"cs_id"`
	CsLocationDistrictId int `json:"cs_location_district_id"`
	CsLocationAreaId     int `json:"cs_location_area_id"`
	CDistrictId          int `json:"c_district_id"`
	CLocationAreaId      int `json:"c_location_area_id"`
	ConsumerId           int `json:"consumer_id"`
	TotalArea            int `json:"total_area"`
	LivingArea           int `json:"living_area"`
	NotLivingArea        int `json:"not_living_area"`
	Priority             int `json:"priority"`
	DaysOfWork           int `json:"days_of_work"`
	Year                 int `json:"year"`
	Month                int `json:"month"`
	Season               int `json:"season"`
	Day                  int `json:"day"`
	DayOfWeek            int `json:"day_of_week"`
	IsWeekend            int `json:"is_weekend"`
	LastEventId          int `json:"last_event_id"`
}
type Event struct {
	EventName string `json:"event_name"`
}

func TransformPredictable(data any) []float32 {
	var arr []float32
	reflectValue := reflect.ValueOf(data)
	// Проверяем, является ли нам переданный интерфейс структурой
	if reflectValue.Kind() == reflect.Struct {
		// Количество полей в структуре
		//typeOfPerson := reflectValue.Type()
		for i := 0; i < reflectValue.NumField(); i++ {
			field := reflectValue.Field(i)
			//fmt.Printf("%s (%s): %v\n", typeOfPerson.Field(i).Name, field.Type(), field.Interface())
			arr = append(arr, float32(field.Interface().(int)))
		}
	}
	return arr
}

func (h handler) GetPredict(c *gin.Context) {
	model, err := catboost.Load(
		os.Getenv("MODEL_PATH") + "/events.cbm")
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusNotFound, "model not found")
	}
	defer func(model *catboost.Model) {
		err = model.Free()
		if err != nil {

		}
	}(model)
	id := c.Param("id")
	var predictable Predictable
	err = h.DB.Raw("select * from data_for_prediction where consumer_id = ?", id).Scan(&predictable).Error
	data := TransformPredictable(predictable)
	floats := [][]float32{data}
	cats := [][]string{}
	prediction, err := model.CalcModelPredictionProba(floats, cats)
	//events := []Event{Event{EventName: "Нет"}}
	var events []string
	err = h.DB.Raw("select event_name from postgres.public.event_types").Scan(&events).Error
	events = append(events, "Нет")
	copy(events[1:], events)
	events[0] = "Нет"
	//var eventTypes []models.EventType
	//err = h.DB.Find(&eventTypes).Error
	res := slices.Index(prediction, slices.Max(prediction))

	//var param catboost.ClassParams
	//// get metadata from model
	//err = model.GetMetaData("class_params", &param)
	//if err != nil {
	//	return
	//}
	//fmt.Println(param.ClassToLabel)
	//fmt.Println(param.ClassNames)
	//fmt.Println(model.GetFloatFeaturesCount())
	//fmt.Println(model.GetCatFeaturesCount())
	//fmt.Println(model.GetDimensionsCount())
	//floats := [][]float32{{
	//	5.0, 0.0, 0.0, 1973.0, 0.0,
	//	2048755.0, 9.0, 12.0, 431.0, 21103.0,
	//	21088.0, 15.0, 0.0, 0.0, 0.0,
	//	2048929.0, 22728486.0, 12.0, 0.0, 0.0,
	//	22289201.0, 0.0, 42875644.0, 58761330.0,
	//	45063584.0, 0.0, 0.0}}
	//cats := [][]string{}
	//prediction, err := model.CalcModelPredictionProba(floats, cats)
	//prediction, err := model.CalcModelPrediction(floats, cats)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusNotModified, "predict error")
	}
	//fmt.Println("result_proba", prediction)
	//fmt.Println("max_proba", slices.Max(prediction))
	//prediction, err = model.CalcModelPrediction(floats, cats)
	//fmt.Println("result_predict", prediction)
	//fmt.Println("max_predict", slices.Max(prediction))

	c.JSON(http.StatusOK, gin.H{"predict": events[res], "index": res})

}
