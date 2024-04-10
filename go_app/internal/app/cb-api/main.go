package main

import (
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"os"
	"services01/internal/app/cb-api/pkg/model"
	"services01/pkg/middlewares"
	"services01/pkg/presets"
)

func main() {
	gin.SetMode(gin.DebugMode)
	appName := "cb-api"
	c, err := presets.GetConfig(appName)
	if err != nil {
		log.Fatal(err)
	}
	r := gin.Default()
	r.Use(middlewares.Cors())
	r.Use(middlewares.NoCache())
	r.Use(middlewares.Auth())

	model.RegRoutes(r, c, nil)

	r.NoRoute(func(c *gin.Context) {
		c.JSON(http.StatusNotFound, "not found")
	})
	addr := os.Getenv("API_CB_HOST") + ":" + os.Getenv("API_CB_PORT")
	log.Println("Started on: ", addr)
	if err = r.Run(addr); err != nil {
		log.Fatal("Server DOWN: ", err)
	}
}
