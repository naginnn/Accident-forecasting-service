package main

import (
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"os"
	"services01/internal/app/obj-api/pkg/analytics"
	"services01/internal/app/obj-api/pkg/config"
	"services01/internal/app/obj-api/pkg/events"
	"services01/internal/app/obj-api/pkg/objects"
	"services01/internal/app/obj-api/pkg/temp"
	"services01/internal/app/obj-api/pkg/view"
	"services01/pkg/middlewares"
	"services01/pkg/presets"
)

func main() {
	// load model
	//entries, err := os.ReadDir("/models")
	//if err != nil {
	//	return
	//}
	//
	//for _, e := range entries {
	//	log.Println(e.Name())
	//}

	//gin.SetMode(gin.ReleaseMode)
	gin.SetMode(gin.DebugMode)
	appName := "obj-api"
	c, err := presets.GetConfig(appName)
	if err != nil {
		log.Fatal(err)
	}
	r := gin.Default()

	r.Use(middlewares.Cors())
	r.Use(middlewares.NoCache())
	temp.RegRoutes(r, c)
	r.Use(middlewares.Auth())
	view.RegRoutes(r, c)
	events.RegRoutes(r, c)
	analytics.RegRoutes(r, c)
	config.RegRoutes(r, c)
	objects.RegRoutes(r, c)

	//go func() {
	//	time.Sleep(4 * time.Minute)
	//	err := weather.UpdateTempDataArea(c.DB)
	//	if err != nil {
	//		log.Println(err)
	//	}
	//	for {
	//		err = weather.CalculateFallTemp(c.DB)
	//		if err != nil {
	//			log.Println(err)
	//		}
	//		time.Sleep(2 * time.Minute)
	//	}
	//}()

	r.NoRoute(func(c *gin.Context) {
		c.JSON(http.StatusNotFound, "not found")
	})
	addr := os.Getenv("API_OBJ_HOST") + ":" + os.Getenv("API_OBJ_PORT")
	log.Println("Started on: ", addr)
	if err = r.Run(addr); err != nil {
		log.Fatal("Server DOWN: ", err)
	}
}
