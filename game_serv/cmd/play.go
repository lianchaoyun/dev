package cmd

import (
	"github.com/name5566/leaf"
	lconf "github.com/name5566/leaf/conf"
	"github.com/spf13/viper"
	"log"
	"serv/game"
	"serv/gate"
	"serv/login"
)

func RunPlay() {

	lconf.LogLevel = viper.GetString("LogLevel")
	lconf.LogPath = viper.GetString("LogPath")
	lconf.LogFlag = log.LstdFlags
	//lconf.ConsolePort = viper.GetInt("ConsolePort")
	//lconf.ProfilePath = viper.GetString("ProfilePath")

	leaf.Run(
		game.Module,
		gate.Module,
		login.Module,
	)
}
