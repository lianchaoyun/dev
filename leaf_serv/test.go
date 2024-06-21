package main

import (
	"bytes"
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"github.com/zheng-ji/goSnowFlake"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"sort"
	"strconv"
	"strings"
	"sync"
	"time"
)

var (
	wg sync.WaitGroup
)

type JsonPostData struct {
}

func Md5(str string) string {
	h := md5.New()
	h.Write([]byte(str))
	return hex.EncodeToString(h.Sum(nil))
}

/*
*
根据key排序
*/
func sortMapKey(mp map[string]string) []string {
	var newMp = make([]string, 0)
	for k, _ := range mp {
		newMp = append(newMp, k)
	}
	sort.Strings(newMp)
	return newMp
}

func (this *JsonPostData) Http(url string, info map[string]string) string {
	bytesData, err := json.Marshal(info)
	if err != nil {
		fmt.Println(err.Error())
		return "error"
	}
	reader := bytes.NewReader(bytesData)
	request, err := http.NewRequest("POST", url, reader)
	defer request.Body.Close()
	if err != nil {
		fmt.Println(err.Error())
		return "error"
	}
	request.Header.Set("Content-Type", "application/json;charset=UTF-8")
	client := http.Client{}
	resp, err := client.Do(request)
	if err != nil {
		fmt.Println("请求异常", err.Error())
		return "error"
	}

	respBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("解析异常", err.Error())
		return "error"
	}
	return string(respBytes)
}

func (this *JsonPostData) Http2(url string, info map[string]string) string {
	bytesData, err := json.Marshal(info)
	if err != nil {
		fmt.Println(err.Error())
		return "error"
	}
	reader := bytes.NewReader(bytesData)
	request, err := http.NewRequest("POST", url, reader)
	defer request.Body.Close()
	if err != nil {
		fmt.Println(err.Error())
		return "error"
	}
	request.Header.Set("Content-Type", "application/json;charset=UTF-8")
	request.Header.Set("version", "1.0.0")

	client := http.Client{}
	resp, err := client.Do(request)
	if err != nil {
		fmt.Println("请求异常", err.Error())
		return "error"
	}

	respBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("解析异常", err.Error())
		return "error"
	}
	return string(respBytes)
}

func getId() string {
	iw, err := goSnowFlake.NewIdWorker(1)
	if err != nil {
		fmt.Println(err)
	}
	id, err := iw.NextId()
	return strconv.FormatInt(id, 10) + strconv.FormatInt(rand.Int63(), 10)
}
func (this *JsonPostData) PayOrder() {
	now := time.Now().Unix()

	url := host + "/test"
	info := make(map[string]string)
	info["appid"] = "mRr5509xlklR44lE"
	//nano := time.Now().UnixNano() / 1e6
	//info["order_sn"] = "MM" + strconv.FormatInt(nano, 10) + strconv.FormatInt(rand.Int63(), 10)
	newInfoKeys := sortMapKey(info)
	buffer := ""
	i := 0
	for _, v := range newInfoKeys {
		if i != 0 {
			buffer += "&"
		}
		buffer += v + "=" + info[v]
		i++
	}
	buffer += "&appsecret=" + appsecret
	info["signature"] = strings.ToUpper(Md5(buffer))
	fmt.Println(info)
	body := this.Http(url, info)
	fmt.Println("请求时间 ", time.Now().Unix()-now, "     ", body)

}

var host = "http://api.test.com"
var appid = "test"
var appsecret = "test"

func tedt1() {
	for j := 1; j < 2; j++ {
		for i := 0; i < 1; i++ {
			wg.Add(1)
			fmt.Println("j=", j, " i=", i)
			title := ""
			go func(i int, title string) {
				a := new(JsonPostData)
				//a.DfApply()
				a.PayOrder()
				//a.PayOrderOld()
				defer wg.Done()
			}(i, title)
		}
		time.Sleep(1 * time.Second)
	}
	wg.Wait()
	log.Println(strings.Repeat("-", 37))
	fmt.Println(Md5("guoke"))
}

func test() string {
	return ""
}

func main() {
	tedt1()
	a := new(JsonPostData)
	a.PayOrder()
}
