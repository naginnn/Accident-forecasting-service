package auth

import (
	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
	"net/http"
	"services01/pkg/models"
	"services01/pkg/tools"
	"strings"
	"time"
)

func (h handler) GetTkn(c *gin.Context) {
	contain := strings.Split(c.GetHeader("Authorization"), " ")
	if contain[0] == "Basic" && contain[1] != "" {
		enc := string(tools.Decode(contain[1]))
		cred := strings.Split(enc, ":")
		if len(cred) == 2 {
			cr, err := tools.Encrypt(cred[1])
			if err != nil {
				c.JSON(http.StatusUnauthorized, "invalid credentials")
				return
			}
			var usr *models.UsrData
			if h.DB.Where("name = ?", cred[0]).Find(&usr).RowsAffected == 0 {
				c.JSON(http.StatusUnauthorized, "invalid credentials")
				return
			}
			if cr != usr.Pwd {
				c.JSON(http.StatusUnauthorized, "invalid credentials")
				return
			}
			token := jwt.New(jwt.SigningMethodHS256)
			claims := token.Claims.(jwt.MapClaims)
			claims["usr"] = usr.Name
			claims["roles"] = usr.Roles
			accessTokenExpireTime := time.Now().Add(time.Hour * 48).Unix()
			claims["exp"] = accessTokenExpireTime
			t, err := token.SignedString([]byte("je3k2d!!dgr1asd"))
			c.JSON(http.StatusOK, gin.H{"tkn": t})
			return
		}
	} else {
		c.JSON(http.StatusUnauthorized, "invalid credentials")
		return
	}
}
