package middlewares

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"os"
	"time"
)

func Cors() gin.HandlerFunc {
	return cors.New(cors.Config{
		AllowOrigins: []string{os.Getenv("CORS"), "0.0.0.0:3010", "localhost:3010"},
		AllowMethods: []string{"PUT", "PATCH", "POST", "GET", "DELETE"},
		AllowHeaders: []string{"Origin", "Authorization", "Content-Type", "Accept-Encoding"},
		ExposeHeaders: []string{
			"Content-Length", "Access-Control-Allow-Origin",
			"Access-Control-Allow-Credentials", "Access-Control-Allow-Headers",
			"Access -Control-Allow-Methods"},
		AllowCredentials: true,
		AllowOriginFunc:  func(origin string) bool { return origin == os.Getenv("CORS") },
		MaxAge:           12 * time.Hour,
	})
}
