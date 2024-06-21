package main

import (
	"github.com/spf13/viper"
	"golang.org/x/sync/errgroup"
	"log"
	"serv/cmd"
	"serv/conf"
)

var (
	g errgroup.Group
)

func main() {
	conf.GetDB()
	if viper.GetBool("web.open") {
		g.Go(func() error {
			return cmd.WebRouter().ListenAndServe()
		})
	}
	if viper.GetBool("chat.open") {
		g.Go(func() error {
			return cmd.RunChat()
		})
	}
	if viper.GetBool("play.open") {
		g.Go(func() error {
			cmd.RunPlay()
			return nil
		})
	}
	if err := g.Wait(); err != nil {
		log.Fatal(err)
	}

}
