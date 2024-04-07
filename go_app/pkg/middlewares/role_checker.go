package middlewares

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"strings"
)

func RoleChecker(fn gin.HandlerFunc, role string) gin.HandlerFunc {
	return func(c *gin.Context) {
		acs := false
		usrRoles, ok := c.Get("usrRoles")
		if !ok {
			c.JSON(http.StatusForbidden, "Forbidden")
			return
		}
		ur := usrRoles.([]string)
		for _, usrRole := range ur {
			if contain := strings.Contains(role, usrRole); contain {
				acs = true
				break

			}
		}
		if acs {
			fn(c)
		} else {
			c.JSON(http.StatusForbidden, "Forbidden")
			return
		}

	}
}
