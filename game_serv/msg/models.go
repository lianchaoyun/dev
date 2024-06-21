package msg

import "time"

// 数据模型
type User struct {
	ID                int       `gorm:"primaryKey" json:"id"`
	UserLogin         string    `json:"user_login"`
	UserPass          string    `json:"user_pass"`
	UserToken         string    `json:"user_token"`
	UserTokenCreateat time.Time `json:"user_token_createat"  gorm:"type:datetime;default:2000-01-01 00:00:00"`
	UserNicename      string    `json:"user_nicename"`
	UserEmail         string    `json:"user_email"`
	UserUrl           string    `json:"user_url"`
	UserRegistered    time.Time `json:"user_registered" gorm:"type:datetime;default:2000-01-01 00:00:00"`
	UserActivationKey string    `json:"user_activation_key"`
	UserStatus        string    `json:"user_status" gorm:"default:0"`
	DisplayName       string    `json:"display_name"`
	UserName          string    `json:"user_name"`
	UserNumber        string    `json:"user_number"`
}

func (u User) TableName() string {
	return "y_users"
}

type Area struct {
	Id         int    `gorm:"primaryKey" json:"id"`
	AreaName   string `json:"area_name"`
	AreaStatus string `json:"area_status"`
	Token      string `json:"token"`
}

func (a Area) TableName() string {
	return "y_area"
}

type Role struct {
	Id                     int       `gorm:"primaryKey" json:"id"`
	Token                  string    `json:"token"`
	UserId                 int       `json:"user_id"`
	AreaId                 int       `json:"area_id"`
	RoleNickname           string    `json:"role_nickname"`
	RoleCareer             string    `json:"role_career"`
	RoleGender             string    `json:"role_gender"`
	RoleAngle              int       `json:"role_angle"`
	RoleMap                string    `json:"role_map"`
	RoleMapName            string    `json:"role_map_name"`
	RoleMapX               int       `json:"role_map_x"`
	RoleMapY               int       `json:"role_map_y"`
	RoleAssetLevel         int       `json:"role_asset_level"`
	RoleAssetLife          int       `json:"role_asset_life"`
	RoleAssetLifeMax       int       `json:"role_asset_life_max"`
	RoleAssetMagic         int       `json:"role_asset_magic"`
	RoleAssetMagicMax      int       `json:"role_asset_magic_max"`
	RoleAssetExperience    int       `json:"role_asset_experience"`
	RoleAssetExperienceMax int       `json:"role_asset_experience_max"`
	RoleBodyClothe         string    `json:"role_body_clothe"`
	RoleBodyWeapon         string    `json:"role_body_weapon"`
	RoleBodyWing           string    `json:"role_body_wing"`
	RoleCreateat           time.Time `json:"role_createat"`
}

func (r Role) TableName() string {
	return "y_role"
}

// 请求模型
type LoginReq struct {
	Account  string `json:"account"`
	Password string `json:"password"`
}

type ModifyPasswordReq struct {
	Account     string `json:"account"`
	Password    string `json:"password"`
	NewPassword string `json:"new_password"`
}

type RegisterReq struct {
	Account   string `json:"account"`
	Password  string `json:"password"`
	Name      string `json:"name"`
	Number    string `json:"number"`
	QuestionA string `json:"question_a"`
	AnswerA   string `json:"answer_a"`
	QuestionB string `json:"question_b"`
	AnswerB   string `json:"answer_b"`
}
type RoleCreateReq struct {
	Career   string `json:"career"`
	Gender   string `json:"gender"`
	Nickname string `json:"nickname"`
	Token    string `json:"token"`
}
