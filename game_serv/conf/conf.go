package conf

import (
	"errors"
	"flag"
	"fmt"
	"github.com/spf13/viper"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"log"
	"time"
)

var (
	// log conf
	LogFlag = log.LstdFlags

	// gate conf
	PendingWriteNum        = 2000
	MaxMsgLen       uint32 = 4096
	HTTPTimeout            = 10 * time.Second
	LenMsgLen              = 2
	LittleEndian           = false

	// skeleton conf
	GoLen              = 10000
	TimerDispatcherLen = 10000
	AsynCallLen        = 10000
	ChanRPCLen         = 10000
)

var Server struct {
	LogLevel    string
	LogPath     string
	WSAddr      string
	CertFile    string
	KeyFile     string
	TCPAddr     string
	MaxConnNum  int
	ConsolePort int
	ProfilePath string
}

var (
	_db      *gorm.DB
	confPath = flag.String("d", "./bin/conf/config.yaml", "")
)

func init() {
	loadConfig()
	Server.LogLevel = viper.GetString("play.LogLevel")
	Server.LogPath = viper.GetString("play.LogPath")
	Server.TCPAddr = viper.GetString("play.TCPAddr")
	Server.WSAddr = viper.GetString("play.WSAddr")
	Server.MaxConnNum = viper.GetInt("play.MaxConnNum")
	initDBPool()
}

func loadConfig() {
	flag.Parse()
	viper.SetConfigFile(*confPath)
	viper.SetConfigType("yaml")
	if err := viper.ReadInConfig(); err != nil {
		var configFileNotFoundError viper.ConfigFileNotFoundError
		if errors.As(err, &configFileNotFoundError) {
			fmt.Println(errors.New("config file not found"))
		}
		return
	}
}

func initDBPool() {
	username := viper.Get("mysql.username")
	password := viper.Get("mysql.password")
	host := viper.Get("mysql.host")
	port := viper.GetInt("mysql.port")
	Dbname := viper.Get("mysql.dbname")
	timeout := "10s"
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8&parseTime=True&loc=Local&timeout=%s", username, password, host, port, Dbname, timeout)
	var err error
	_db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("连接数据库失败, error=" + err.Error())
	}

	sqlDB, _ := _db.DB()
	sqlDB.SetMaxOpenConns(100)
	sqlDB.SetMaxIdleConns(20)
}
func GetDB() *gorm.DB {
	return _db
}
