package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"golang.org/x/sync/errgroup"
	"log"
	"net/http"
)

var (
	g errgroup.Group
)

func httpServer() http.Handler {
	r := gin.New()
	r.Use(gin.Recovery())
	r.Static("/assets", "./www/assets")
	r.StaticFS("/file", http.Dir("./www/file_system"))
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	group := r.Group("/group")
	{
		group.GET("/g1", func(c *gin.Context) {
			c.JSON(http.StatusOK, gin.H{
				"message": "g1",
			})
		})
	}

	r.Group("/group1").GET("/g1", func(c *gin.Context) {
		c.String(http.StatusOK, "ohai")
	})

	r.MaxMultipartMemory = 8 << 20 // 8 MiB
	r.POST("/upload", func(c *gin.Context) {
		// Single file
		file, _ := c.FormFile("file")
		log.Println(file.Filename)

		// Upload the file to specific dst.
		c.SaveUploadedFile(file, "./www/upload/a.png")

		c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
	})
	return r
}

func main() {
	/*
		server01 := &http.Server{
			Addr:         ":8888",
			Handler:      httpServer(),
			ReadTimeout:  5 * time.Second,
			WriteTimeout: 10 * time.Second,
		}
		g.Go(func() error {
			err := server01.ListenAndServe()
			if err != nil && err != http.ErrServerClosed {
				log.Fatal(err)
			}
			return err
		})
		g.Go(func() error {
			lconf.LogLevel = conf.Server.LogLevel
			lconf.LogPath = conf.Server.LogPath
			lconf.LogFlag = conf.LogFlag
			lconf.ConsolePort = conf.Server.ConsolePort
			lconf.ProfilePath = conf.Server.ProfilePath

			leaf.Run(
				game.Module,
				gate.Module,
				login.Module,
			)
			return nil
		})
		fmt.Println("http://localhost:8081")
		if err := g.Wait(); err != nil {
			log.Fatal(err)
		}
	*/
	router := gin.Default()
	router.Static("/static", "./www/static")
	router.StaticFS("/file", http.Dir("./www/file"))
	router.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})
	router.Run(":8081")
	/*router.Use(func(c *gin.Context) {
		secureMiddleware := secure.New(secure.Options{
			SSLRedirect: true,
			SSLHost:     "localhost:9090",
		})
		err := secureMiddleware.Process(c.Writer, c.Request)
		if err != nil {
			return
		}
		c.Next()
	})
	router.RunTLS(":9090", "./ssl/meimei.com_chain.crt", "./ssl/meimei.com_key.key")
	*/
}
