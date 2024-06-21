package cmd

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"net/http"
	"serv/controller"
	"time"
)

func WebRouter() *http.Server {
	r := gin.New()
	r.Use(gin.Recovery())
	r.Static("/web", "./web")
	r.StaticFS("/file", http.Dir("./www/"))
	r.Any("/game/user/login", controller.Api.Login)
	r.Any("/game/user/change/password", controller.Api.ModifyPassword)
	r.Any("/game/user/register", controller.Api.Register)
	r.Any("/game/user/role/list", controller.Api.RoleList)
	r.Any("/game/user/role/create", controller.Api.RoleCreate)
	addr := fmt.Sprintf("%s:%d", viper.Get("web.host"), viper.GetInt("web.port"))
	return &http.Server{
		Addr:         addr,
		Handler:      r,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

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
