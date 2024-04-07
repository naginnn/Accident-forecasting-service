package middlewares

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/tools"
	"strings"
)

func checkTkn(tkn string) (bool, []string) {

	return true, []string{"Role1", "Role2"}
}

func Auth() gin.HandlerFunc {
	return func(c *gin.Context) {
		var usrRoles []string
		var err error
		contain := strings.Split(c.GetHeader("Authorization"), " ")
		if len(contain) > 0 {
			if contain[0] == "Bearer" {
				usrRoles, err = tools.CheckBearer(contain[1])
				if err != nil {
					c.JSON(http.StatusUnauthorized, "Unauthorized")
					return
				}
			}
		}

		if len(usrRoles) == 0 {
			c.JSON(http.StatusUnauthorized, "Unauthorized")
			return
		}

		c.Set("usrRoles", usrRoles)
		c.Next()
	}
}

//	}
//		switch key {
//		case "exp":
//			if val. (float64) < float64 (time .Now() .Unix())
//				E return nit, errors.New( (text "token is expire") I
//		case "username":
//			cred.Usr = val. (string)
//		case "user_groups":
//			groups, ok := val. (linterface)) if lok L return nit, err }
//		cred.Groups = make([Istring, Len(groups))
//		for 1, v := range groups {
//			cred.Groups[1] = fmt. Sprint(v)
//
//}
