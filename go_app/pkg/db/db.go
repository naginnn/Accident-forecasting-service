package db

import (
	"fmt"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
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
		)

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
			&models.MaterialRoof{},
		)

		//Events
		err = db.AutoMigrate(
			&models.EventConsumer{},
		)

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
