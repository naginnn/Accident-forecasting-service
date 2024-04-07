package main

import (
	"fmt"
)

func main() {
	b64 := "ZnVuYyBtYWluKCl7CiAgICBmbXQuUHJpbnRsbigibGFsYWwiKTsKfQ=="
	encStr := EncSex(b64)
	fmt.Println(encStr)
	fmt.Println(DecSex(encStr))
	fmt.Println(b64)
}

func EncSex(cat string) []int32 {
	var arr []int32
	for _, b64st := range cat {
		arr = append(arr, b64st-5)
	}
	return arr
}

func DecSex(arr []int32) string {
	var strArr string
	for _, a := range arr {
		strArr += fmt.Sprintf("%c", a+5)
	}
	return strArr
}
