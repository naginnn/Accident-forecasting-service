package db

import (
	"fmt"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/clause"
	"gorm.io/gorm/logger"
	"log"
	"os"
	"services01/pkg/models"
	"services01/pkg/tools"
)

func Init(appName string) (*gorm.DB, error) {
	//pgStr := os.Getenv("PG_DSN")
	//sch := strings.Split(pgStr, "/")
	//schemaName := sch[len(sch)-1]
	//db, err := gorm.Open(postgres.New(postgres.Config{PreferSimpleProtocol: true, DSN: pgStr}),
	//	&gorm.Config{
	//		PrepareStmt: false,
	//		NamingStrategy: schema.NamingStrategy{
	//			TablePrefix:   schemaName + ".",
	//			SingularTable: false,
	//		},
	//	})
	dsn := fmt.Sprintf("postgres://%s:%s@%s:%s/%s",
		os.Getenv("POSTGRES_USER"),
		os.Getenv("POSTGRES_PASSWORD"),
		os.Getenv("POSTGRES_HOST"),
		os.Getenv("POSTGRES_PORT"),
		os.Getenv("POSTGRES_DB"),
	)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})

	if err != nil {
		log.Fatal(err)
		return nil, err
	}

	switch appName {
	case "reg-auth-api":
		err = db.AutoMigrate(&models.UsrData{})
		pwdAdm, _ := tools.Encrypt("adm")
		pwdUsr, _ := tools.Encrypt("usr")

		if err == nil {
			db.Create(&models.UsrData{Name: "adm", Pwd: pwdAdm, Roles: "ro,rw"})
			db.Create(&models.UsrData{Name: "usr", Pwd: pwdUsr, Roles: "ro"})
		}
	case "obj-api":

		// Locations
		err = db.AutoMigrate(
			&models.LocationDistrict{},
			&models.LocationArea{},
		)

		// Weather
		err = db.AutoMigrate(
			&models.WeatherArea{},
			&models.WeatherConsumerFall{},
			&models.WeatherCondition{},
		)
		defaultWeatherCondition := []*models.WeatherCondition{
			&models.WeatherCondition{Name: "clear", K: 0.01, Description: "ясно"},
			&models.WeatherCondition{Name: "partly-cloudy", K: 0.01, Description: "переменная облачность"},
			&models.WeatherCondition{Name: "cloudy", K: 0.01, Description: "облачно"},
			&models.WeatherCondition{Name: "overcast", K: 0.01, Description: "с прояснениями"},
			&models.WeatherCondition{Name: "drizzle", K: 0.01, Description: "моросящий дождь"},
			&models.WeatherCondition{Name: "light-rain", K: 0.01, Description: "небольшой дождь"},
			&models.WeatherCondition{Name: "rain", K: 0.01, Description: "умеренный дождь"},
			&models.WeatherCondition{Name: "moderate-rain", K: 0.01, Description: "сильный дождь"},
			&models.WeatherCondition{Name: "heavy-rain", K: 0.01, Description: "непрерывный"},
			&models.WeatherCondition{Name: "continuous-heavy-rain", K: 0.01, Description: "дождь"},
			&models.WeatherCondition{Name: "showers", K: 0.01, Description: "сильный ливень"},
			&models.WeatherCondition{Name: "wet-snow", K: 0.01, Description: "мокрый снег"},
			&models.WeatherCondition{Name: "light-snow", K: 0.01, Description: "небольшой снег"},
			&models.WeatherCondition{Name: "snow", K: 0.01, Description: "метель"},
			&models.WeatherCondition{Name: "snow-showers", K: 0.01, Description: "ливень"},
			&models.WeatherCondition{Name: "hail", K: 0.01, Description: "с градом"},
			&models.WeatherCondition{Name: "thunderstorm", K: 0.01, Description: "гроза"},
			&models.WeatherCondition{Name: "thunderstorm-with-rain", K: 0.01, Description: "гроза с дождем"},
			&models.WeatherCondition{Name: "thunderstorm-with-hail", K: 0.01, Description: "гроза с градом"},
		}
		err = db.Clauses(clause.OnConflict{
			Columns:   []clause.Column{{Name: "name"}},
			DoUpdates: clause.AssignmentColumns([]string{"k", "description"}),
		}).Create(&defaultWeatherCondition).Error

		err = db.AutoMigrate(
			&models.ObjConsumerStation{},
			&models.ObjSourceStation{},
			&models.ObjConsumer{},
		)
		// Locations
		err = db.AutoMigrate(
			&models.LocationDistrict{},
			&models.LocationArea{},
		)
		// Materials
		err = db.AutoMigrate(
			&models.MaterialWall{},
		)

		//Events
		err = db.AutoMigrate(
			&models.EventConsumer{},
			&models.EventCounter{},
		)
		//EventsType
		err = db.AutoMigrate(
			&models.EventType{},
		)

		//ModelInfo
		err = db.AutoMigrate(
			&models.ModelInfo{},
		)

		events := []string{
			"P1 <= 0",
			"P2 <= 0",
			"T1 > max",
			"T1 < min",
			"Авария",
			"Недостаточная температура подачи ЦО (Недотоп)",
			"Превышение температуры подачи ЦО (Перетоп)",
			"Утечка теплоносителя",
			"Течь в системе отопления",
			"Температура в квартире ниже нормативной",
			"Крупные пожары",
			"Температура в помещении общего пользования ниже нормативной",
			"Аварийная протечка труб в подъезде",
			"Протечка труб в подъезде",
			"Отсутствие отопления в доме",
			"Сильная течь в системе отопления",
		}
		var defaultEvents []*models.EventType
		for i, eventName := range events {
			defaultEvents = append(defaultEvents, &models.EventType{ID: uint64(i + 1), EventName: eventName})
		}
		//for _, eventType := range events {
		err = db.Clauses(clause.OnConflict{
			Columns:   []clause.Column{{Name: "event_name"}},
			DoUpdates: clause.AssignmentColumns([]string{"event_name"}),
		}).Create(&defaultEvents).Error
		//}

	}

	if err != nil {
		log.Println(err)
	}
	return db, nil
}

//fmt.Println(pp)
//dsn := os.Getenv("PG_DSN")
//rx := regexp.MustCompile(`(?s)` + regexp.QuoteMeta("/") + `(.*?)` + regexp.QuoteMeta(":"))
//res := rx.FindAllStringSubmatch(dsn, -1)
//if len(res) > 0 {
//	if len(res[0]) > 0 {
//		schemaName = res[0][1]
//	}
//}
