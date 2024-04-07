package tools

import (
	"crypto/aes"
	"crypto/cipher"
	"encoding/base64"
	"errors"
	"github.com/golang-jwt/jwt/v5"
	"strings"
	"time"
)

var bytes = []byte{35, 46, 57, 24, 85, 35, 24, 74, 87, 35, 88, 98, 66, 32, 14, 05}

const sec = "abc&1*~#^2^#s0^=)^^7%b34"

func Encode(b []byte) string {
	return base64.StdEncoding.EncodeToString(b)
}

func Encrypt(text string) (string, error) {
	text = base64.StdEncoding.EncodeToString([]byte(text))
	block, err := aes.NewCipher([]byte(sec))
	if err != nil {
		return "", err
	}
	plainText := []byte(text)
	cfb := cipher.NewCFBEncrypter(block, bytes)
	cipherText := make([]byte, len(plainText))
	cfb.XORKeyStream(cipherText, plainText)
	return Encode(cipherText), nil
}

func Decode(s string) []byte {
	data, err := base64.StdEncoding.DecodeString(s)
	if err != nil {
		return nil
	}
	return data
}

func Decrypt(text string) (string, error) {
	block, err := aes.NewCipher([]byte(sec))
	if err != nil {
		return "", err
	}
	cipherText := Decode(text)
	cfb := cipher.NewCFBDecrypter(block, bytes)
	plainText := make([]byte, len(cipherText))
	cfb.XORKeyStream(plainText, cipherText)
	//res := Decode(string(plainText))
	return string(plainText), nil
}

func CheckBasic(data string) ([]string, error) {
	cred, err := base64.URLEncoding.DecodeString(data)
	if err != nil {
		return nil, err
	}
	credArr := strings.Split(string(cred), ":")
	return credArr, nil
}

func CheckBearer(tkn string) ([]string, error) {
	var usrGr []string
	sec := "je3k2d!!dgr1asd"
	claims := jwt.MapClaims{}
	_, err := jwt.ParseWithClaims(tkn, claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(sec), nil
	})
	if err != nil {
		return nil, err
	}

	for key, val := range claims {
		switch key {
		case "exp":
			if val.(float64) < float64(time.Now().Unix()) {
				return nil, errors.New("token is expire")
			}
		case "roles":
			//gr, ok := val.([]interface{})
			gr, ok := val.(string)
			if !ok {
				return nil, errors.New("groups not found")
			}
			usrGr = strings.Split(gr, ",")
		}
	}
	return usrGr, nil
}
