package weather

import (
	"math"
)

type WeatherCondition string

const (
	Sunny    WeatherCondition = "Sunny"
	Cloudy   WeatherCondition = "Cloudy"
	Overcast WeatherCondition = "Overcast"
)

type WindDirection string

const (
	North     WindDirection = "North"
	NorthEast WindDirection = "NorthEast"
	East      WindDirection = "East"
	SouthEast WindDirection = "SouthEast"
	South     WindDirection = "South"
	SouthWest WindDirection = "SouthWest"
	West      WindDirection = "West"
	NorthWest WindDirection = "NorthWest"
)

func ConvertToDegreesOld(direction WindDirection) float64 {
	switch direction {
	case North:
		return 0
	case NorthEast:
		return 45
	case East:
		return 90
	case SouthEast:
		return 135
	case South:
		return 180
	case SouthWest:
		return 225
	case West:
		return 270
	case NorthWest:
		return 315
	default:
		return 0 // Северное направление по умолчанию
	}
}

func ConvertToDegrees(direction string) float64 {
	switch direction {
	case "n":
		return 0
	case "ne":
		return 45
	case "e":
		return 90
	case "se":
		return 135
	case "s":
		return 180
	case "sw":
		return 225
	case "w":
		return 270
	case "nw":
		return 315
	case "c":
		return -1
	default:
		return 0 // Северное направление по умолчанию
	}
}

func ConvertCondition(condition string) float64 {
	switch condition {
	case "clear":
		return 0
	case "partly-cloudy":
		return 45
	case "cloudy":
		return 0
	case "overcast":
		return 0
	case "drizzle":
		return 0
	case "light-rain":
		return 0
	case "rain":
		return 0
	case "moderate-rain":
		return 0
	case "heavy-rain":
		return 0
	case "continuous-heavy-rain":
		return 0
	case "showers":
		return 0
	case "wet-snow":
		return 0
	case "light-snow":
		return 0
	case "snow":
		return 0
	case "snow-showers":
		return 0
	case "hail":
		return 0
	case "thunderstorm":
		return 0
	case "thunderstorm-with-rain":
		return 0
	case "thunderstorm-with-hail":
		return 0
	default:
		return 0 // Северное направление по умолчанию
	}
}

func adjustCooling(k, weatherEffect, windSpeed, windDegrees, humidity float64) float64 {
	windEffect := windSpeed * 0.01
	humidityEffect := (humidity - 50) * 0.001

	// Дополнительный эффект направления ветра
	directionEffect := math.Cos(windDegrees*math.Pi/180.0) * windEffect

	return k + weatherEffect + windEffect + humidityEffect + directionEffect
}

func getSeason() {

}

type NewtonParams struct {
	K, WindSpeed, Humidity, TInitial, TEnv float64
	Weather, WindDirection                 string
	DateTs                                 int64
}

func NewtonCooling(nParams *NewtonParams) float64 {
	nParams.K = adjustCooling(nParams.K,
		ConvertCondition(nParams.Weather),
		nParams.WindSpeed,
		ConvertToDegrees(nParams.WindDirection),
		nParams.Humidity)
	tNew := nParams.TEnv + (nParams.TInitial-nParams.TEnv)*math.Exp(-nParams.K*float64(1))
	return tNew

	//temperatures := make([]float64, 0) // Создаем слайс с начальной ёмкостью равной hours+1
	//temperatures := make([]float64, 0, hours+1)   // Создаем слайс с начальной ёмкостью равной hours+1
	//temperatures = append(temperatures, tInitial) // Начальная температура

	//for hour := 1; hour <= hours; hour++ {
	//	TNew := TEnv + (temperatures[len(temperatures)-1]-TEnv)*math.Exp(-k*float64(hour))
	//	temperatures = append(temperatures, TNew)
	//}
	//k = adjustCooling(k, weather, windSpeed, windDirection, humidity)

	//hour := 1
	//for {
	//	tNew := tEnv + (temperatures[len(temperatures)-1]-tEnv)*math.Exp(-k*float64(hour))
	//	if tNew == temperatures[len(temperatures)-1] {
	//		break
	//	}
	//
	//	temperatures = append(temperatures, tNew)
	//	// пороговое значение
	//	if tNew > lowerTemp && tNew < lowerTemp+1 || tNew < lowerTemp {
	//		break
	//	}
	//	hour++
	//}

}

//func main() {
//	tInitial := 22.0 // начальная температура в градусах Цельсия
//	tEnv := -2.0     // температура окружающей среды в градусах Цельсия
//	k := 0.01        // коэффициент охлаждения
//	//lowerTemp := 2.9 // нижняя граница расчета
//
//	weather := "cloudy"
//	windSpeed := 5.0 // м/с скорость ветра
//	//windDirection := SouthEast // Направление ветра в градусах
//	windDirection := "se" // Направление ветра в градусах
//	//buildingDirection := 90.0 // Направление, в котором наиболее эффективно охлаждение
//	humidity := 70.0 // влажность
//
//	//k = adjustCooling(k, ConvertCondition(weather), windSpeed, ConvertToDegrees(windDirection), humidity)
//	//temperatures := NewtonCooling(k, weather, windSpeed, windDirection, humidity, tInitial, tEnv)
//	//fmt.Println(temperatures)
//	//for i, temp := range temperatures {
//	//	fmt.Printf("Час %d: температура = %v°C\n", i, temp)
//	//}
//	//fmt.Println(fmt.Sprintf("Часов потребуется: %v", len(temperatures)-1))
//	//fmt.Println(temperatures)
//	//fmt.Println(temperatures[1:])
//
//}

// list ["00:00", "01:00", "02:00"]
// list ["22.0", "21.0", "20.0"]
