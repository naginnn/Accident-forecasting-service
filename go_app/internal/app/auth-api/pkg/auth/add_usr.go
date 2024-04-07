package auth

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"services01/pkg/models"
	"services01/pkg/tools"
)

func (h handler) AddUsr(c *gin.Context) {
	var body struct {
		Cred  string `json:"cred" binding:"required"`
		Roles string `json:"roles" binding:"required"`
	}

	err := c.ShouldBindJSON(&body)
	if err != nil {
		c.JSON(http.StatusBadRequest, "invalid request")
		return
	}

	cred, err := tools.CheckBasic(body.Cred)
	if err != nil {
		c.JSON(http.StatusBadRequest, "invalid credentials")
		return
	}
	pwd, err := tools.Encrypt(cred[1])
	err = h.DB.Create(&models.UsrData{
		Name:  cred[0],
		Pwd:   pwd,
		Roles: body.Roles,
	}).Error

	if err != nil {
		c.JSON(http.StatusBadRequest, "invalid credentials")
		return
	}
}
