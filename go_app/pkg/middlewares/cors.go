package middlewares

import (
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"os"
	"strings"
	"time"
)

func Cors() gin.HandlerFunc {
	cors_str := strings.Split(os.Getenv("CORS"), ",")
	return cors.New(cors.Config{
		AllowOrigins: cors_str,
		AllowMethods: []string{"PUT", "PATCH", "POST", "GET", "DELETE"},
		AllowHeaders: []string{"Origin", "Authorization", "Content-Type", "Accept-Encoding"},
		ExposeHeaders: []string{
			"Content-Length", "Access-Control-Allow-Origin",
			"Access-Control-Allow-Credentials", "Access-Control-Allow-Headers",
			"Access -Control-Allow-Methods"},
		AllowCredentials: true,
		AllowOriginFunc:  func(origin string) bool { return origin == cors_str[0] },
		MaxAge:           12 * time.Hour,
	})
}
