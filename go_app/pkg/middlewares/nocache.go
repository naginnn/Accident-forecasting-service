package middlewares

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"time"
)

var epoch = time.Unix(0, 0).UTC().Format(http.TimeFormat)

var noCacheHeaders = map[string]string{
	"Expires":         epoch,
	"Cache-Control":   "no-cache, no-store, no-transform, must-revalidate, private, max-age-0",
	"Pragma":          "no-cache",
	"X-Accel-Expires": "O",
}

var etagHeaders = []string{
	"ETag",
	"If-Modified-Since",
	"If-Match",
	"If-None-Match",
	"If-Range",
	"If-Unmodified-Since",
}

func NoCache() gin.HandlerFunc {
	return func(c *gin.Context) {
		for _, v := range etagHeaders {
			if c.Request.Header.Get(v) != "" {
				c.Request.Header.Del(v)
			}
		}
		for k, v := range noCacheHeaders {
			c.Writer.Header().Set(k, v)
		}
		c.Next()
	}
}
