package main

import (
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"os"
	"services01/internal/app/obj-api/pkg/objects"
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
	r.Use(middlewares.Auth())

	objects.RegRoutes(r, c)

	r.NoRoute(func(c *gin.Context) {
		c.JSON(http.StatusNotFound, "not found")
	})
	addr := os.Getenv("API_OBJ_HOST") + ":" + os.Getenv("API_OBJ_PORT")
	log.Println("Started on: ", addr)
	if err = r.Run(addr); err != nil {
		log.Fatal("Server DOWN: ", err)
	}
}
