package controller

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"serv/conf"
	"serv/msg"
	"serv/tools"
	"time"
)

var Api = newApi()

func newApi() *api {
	return &api{}
}

type api struct {
}

func (a *api) Login(c *gin.Context) {
	var loginReq msg.LoginReq
	if err := c.ShouldBindJSON(&loginReq); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "非法请求"})
		return
	}
	json := make(map[string]any)
	json["code"] = tools.Ok
	json["msg"] = "success"

	var user msg.User
	db := conf.GetDB()
	db.First(&user, "user_email = ?", loginReq.Account)
	if user.UserPass != loginReq.Password {
		c.JSON(http.StatusOK, gin.H{"code": tools.Err, "msg": "用户名或密码错误"})
		return
	}
	if tools.IsEmpty(user.UserToken) || user.UserTokenCreateat.Unix() > 3600 {
		token := tools.RandString(64)
		db.Model(&user).Updates(map[string]interface{}{"user_token": token, "user_token_createat": time.Now()})
		user.UserToken = token
	}
	data := make(map[string]any)
	data["token"] = user.UserToken
	var areas []msg.Area
	db.Find(&areas)
	data["areas"] = areas
	json["data"] = data
	c.JSON(
		http.StatusOK,
		json,
	)
}

func (a *api) Register(c *gin.Context) {
	var registerReq msg.RegisterReq
	if err := c.ShouldBindJSON(&registerReq); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "非法请求"})
		return
	}

	if !tools.IsEmail(registerReq.Account) {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "email地址不合法"})
		return
	}
	if !tools.IsPassword(registerReq.Password) {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "密码不合法,密码长度6-18个字符"})
		return
	}

	user := msg.User{
		UserEmail:         registerReq.Account,
		UserPass:          registerReq.Password,
		UserName:          registerReq.Name,
		UserNumber:        registerReq.Number,
		UserToken:         tools.RandString(32),
		UserTokenCreateat: time.Now(),
		UserRegistered:    time.Now(),
		UserLogin:         tools.RandString(18),
	}

	db := conf.GetDB()

	db.First(&user, "user_email = ?", registerReq.Account)
	if user.ID > 0 {
		c.JSON(http.StatusOK, gin.H{"code": tools.Err, "msg": "邮箱已被注册，请换一个"})
		return
	}

	result := db.Create(&user)
	if result.RowsAffected < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "注册失败"})
		return
	}

	json := make(map[string]any)
	json["code"] = tools.Ok
	json["msg"] = "success"

	data := make(map[string]any)
	json["data"] = data

	c.JSON(
		http.StatusOK,
		json,
	)
}

func (a *api) ModifyPassword(c *gin.Context) {
	var modifyPasswordReq msg.ModifyPasswordReq
	if err := c.ShouldBindJSON(&modifyPasswordReq); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "非法请求"})
		return
	}
	var user msg.User
	db := conf.GetDB()
	db.First(&user, "user_email = ?", modifyPasswordReq.Account)

	if user.ID < 1 {
		c.JSON(http.StatusOK, gin.H{"code": tools.Err, "msg": "用户不存在"})
		return
	}

	if user.UserPass != modifyPasswordReq.Password {
		c.JSON(http.StatusOK, gin.H{"code": tools.Err, "msg": "原密码错误"})
		return
	}

	if !tools.IsPassword(modifyPasswordReq.NewPassword) {
		c.JSON(http.StatusOK, gin.H{"code": tools.Err, "msg": "密码不合法,密码长度6-18个字符"})
		return
	}
	db.Model(&user).Updates(map[string]interface{}{"user_pass": modifyPasswordReq.NewPassword})

	json := make(map[string]any)
	json["code"] = tools.Ok
	json["msg"] = "success"

	data := make(map[string]any)
	json["data"] = data

	c.JSON(
		http.StatusOK,
		json,
	)
}

func (a *api) RoleList(c *gin.Context) {
	db := conf.GetDB()
	var user msg.User
	userToken := c.Request.Header.Get("User-Token")
	db.First(&user, "user_token = ?", userToken)
	if user.ID < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "token无效"})
		return
	}

	var area msg.Area
	token := c.Query("token")
	db.First(&area, "token = ?", token)
	if area.Id < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "area token无效"})
		return
	}

	var roles []msg.Role
	db.Find(&roles, "user_id = ? and area_id = ?", user.ID, area.Id)

	json := make(map[string]any)
	json["code"] = tools.Ok
	json["msg"] = "success"

	data := make(map[string]any)
	data["roles"] = roles
	json["data"] = data

	c.JSON(
		http.StatusOK,
		json,
	)
}

func (a *api) RoleCreate(c *gin.Context) {
	var roleCreateReq msg.RoleCreateReq
	if err := c.ShouldBindJSON(&roleCreateReq); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "非法请求"})
		return
	}
	db := conf.GetDB()
	var user msg.User
	userToken := c.Request.Header.Get("User-Token")
	db.First(&user, "user_token = ?", userToken)
	if user.ID < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "token无效"})
		return
	}

	var area msg.Area
	db.First(&area, "token = ?", roleCreateReq.Token)
	if area.Id < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "area token无效"})
		return
	}

	role := msg.Role{
		Token:                  tools.RandString(32),
		UserId:                 user.ID,
		AreaId:                 area.Id,
		RoleCareer:             roleCreateReq.Career,
		RoleGender:             roleCreateReq.Gender,
		RoleNickname:           roleCreateReq.Nickname,
		RoleAngle:              2,
		RoleMap:                "001",
		RoleMapName:            "",
		RoleMapX:               0,
		RoleMapY:               0,
		RoleAssetLevel:         1,
		RoleAssetLife:          1,
		RoleAssetLifeMax:       10,
		RoleAssetMagic:         1,
		RoleAssetMagicMax:      10,
		RoleAssetExperience:    1,
		RoleAssetExperienceMax: 100,
		RoleBodyClothe:         "000",
		RoleBodyWeapon:         "000",
		RoleBodyWing:           "000",
		RoleCreateat:           time.Now(),
	}

	result := db.Create(&role)
	if result.RowsAffected < 1 {
		c.JSON(http.StatusBadRequest, gin.H{"code": tools.Err, "msg": "创建失败"})
		return
	}
	json := make(map[string]any)
	json["code"] = tools.Ok
	json["msg"] = "success"

	data := make(map[string]any)
	data["role"] = role
	json["data"] = data

	c.JSON(
		http.StatusOK,
		json,
	)
}
