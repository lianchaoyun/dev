package tools

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"math/rand"
	"net/mail"
	"reflect"
	"regexp"
	"strconv"
	"strings"
	"time"
)

func PrintRequest(c *gin.Context) {
	fmt.Println(strings.Repeat("-", 37))
	fmt.Println(c.Request.URL, c.Request.Method)
	for k, v := range c.Request.Header {
		fmt.Println(k, v)
	}
	query := c.Request.URL.Query()
	params := make(map[string]string)
	for key, val := range query {
		params[key] = strings.Join(val, ", ")
	}
	err := c.Request.ParseForm()
	if err != nil {
		return
	}
	form := c.Request.PostForm
	for key, val := range form {
		params[key] = strings.Join(val, ", ")
	}
	routeParams := c.Params
	for _, param := range routeParams {
		params[param.Key] = param.Value
	}
	fmt.Printf("参数:%v\n", params)
	data, _ := ioutil.ReadAll(c.Request.Body)
	fmt.Printf("内容:%v\n", string(data))

	fmt.Println(strings.Repeat("-", 37))
}

func RandString(length int) string {
	rand.Seed(time.Now().UnixNano())
	rs := make([]string, length)
	for start := 0; start < length; start++ {
		t := rand.Intn(3)
		if t == 0 {
			rs = append(rs, strconv.Itoa(rand.Intn(10)))
		} else if t == 1 {
			rs = append(rs, string(rand.Intn(26)+65))
		} else {
			rs = append(rs, string(rand.Intn(26)+97))
		}
	}
	return strings.Join(rs, "")
}
func IsEmpty(str string) bool {
	if len(str) == 0 {
		return true
	} else {
		return false
	}
}
func StructToMap(obj interface{}) map[string]interface{} {
	result := make(map[string]interface{})
	value := reflect.ValueOf(obj).Elem()
	typ := value.Type()
	for i := 0; i < typ.NumField(); i++ {
		field := typ.Field(i)
		tag := field.Tag.Get("json")
		if tag != "" && !field.Anonymous {
			result[tag] = value.FieldByIndex([]int{i}).Interface()
		}
	}
	println(result)
	return result
}
func VerifyFormat(exp, str string) bool {
	reg := regexp.MustCompile(exp)
	return reg.MatchString(str)
}
func IsEmail(email string) bool {
	_, err := mail.ParseAddress(email)
	return err == nil
}

func IsUsername(str string) bool {
	return VerifyFormat(`^[a-zA-Z0-9_]{3,18}$`, str)
}

func IsPassword(str string) bool {
	return VerifyFormat(`^[a-zA-Z0-9_\.\&\@]{6,18}$`, str)
}

const (
	Ok  = 0
	Err = 1
)
