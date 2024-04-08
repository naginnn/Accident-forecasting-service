package model

import (
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"os"
	"services01/pkg/ml/wrapper/catboost"
)

func (h handler) GetPredict(c *gin.Context) {
	model, err := catboost.Load(
		os.Getenv("MODEL_PATH") + "/testmodel")
	defer model.Free()
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusNotFound, "model not found")
	}
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
	floats := [][]float32{{
		5.0, 0.0, 0.0, 1973.0, 0.0,
		2048755.0, 9.0, 12.0, 431.0, 21103.0,
		21088.0, 15.0, 0.0, 0.0, 0.0,
		2048929.0, 22728486.0, 12.0, 0.0, 0.0,
		22289201.0, 0.0, 42875644.0, 58761330.0,
		45063584.0, 0.0, 0.0}}
	cats := [][]string{}
	prediction, err := model.CalcModelPredictionProba(floats, cats)
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

	c.JSON(http.StatusOK, gin.H{"predict": prediction})

}
