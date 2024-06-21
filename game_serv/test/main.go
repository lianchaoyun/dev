package test_http

import (
	"bytes"
	"crypto/md5"
	"encoding/hex"
	"encoding/json"
	"flag"
	"fmt"
	"github.com/goburrow/cache"
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

func (this *JsonPostData) Http(http_url string, info map[string]string, flag int, method string) string {

	if flag == 1 {
		var r http.Request
		r.ParseForm()
		for key, val := range info {
			r.Form.Add(key, val)
		}
		bytesData, err := json.Marshal(info)
		if err != nil {
			fmt.Println(err.Error())
			return "error"
		}
		var reader = bytes.NewReader(bytesData)
		if method == "" {
			method = "POST"
		}
		request, err := http.NewRequest(method, http_url, reader)
		if err != nil {
			fmt.Println(err.Error())
			return "error"
		}
		request.Header.Set("Content-Type", "application/json;charset=UTF-8")
		request.Header.Set("User-Agent", "GodotEngine/4.2.stable.official (Windows)")

		request.Header.Set("Game-Token", http_token)
		request.Header.Set("User-Token", account_token)
		var resp *http.Response
		resp, err = http.DefaultClient.Do(request)
		//defer resp.Body.Close()
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
	} else {
		bytesData, err := json.Marshal(info)
		if err != nil {
			fmt.Println(err.Error())
			return "error"
		}
		var reader = bytes.NewReader(bytesData)
		request, err := http.NewRequest("POST", http_url, reader)
		//defer request.Body.Close()
		if err != nil {
			fmt.Println(err.Error())
			return "error"
		}
		request.Header.Set("Content-Type", "application/json;charset=UTF-8")
		request.Header.Set("Game-Token", http_token)
		request.Header.Set("User-Token", account_token)

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

}

func getId() string {

	iw, err := goSnowFlake.NewIdWorker(1)
	if err != nil {
		fmt.Println(err)
	}
	id, err := iw.NextId()
	return strconv.FormatInt(id, 10) + strconv.FormatInt(rand.Int63(), 10)
}

func atk() {
	for i := 1; i < 1000000; i++ {
		//time.Sleep(1)
		wg.Add(1)
		fmt.Println(i)
		title := ""
		go func(i int, title string) {
			//info := make(map[string]string)
			//info["appid"] = "1111111111"
			fmt.Println(i)
			defer wg.Done()
		}(i, title)
	}
	wg.Wait()
	log.Println(strings.Repeat("-", 37))
}

func (this *JsonPostData) login() {
	now := time.Now().Unix()
	url := host + "/game/user/login"
	info := make(map[string]string)
	info["account"] = "153630863@qq.com"
	info["password"] = "423522"
	//nano := time.Now().UnixNano() / 1e6
	//info["order_sn"] = "MM" + strconv.FormatInt(nano, 10) + strconv.FormatInt(rand.Int63(), 10)
	//info["order_sn"] = getId()
	/*
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
	*/
	fmt.Println(info)
	body := this.Http(url, info, 1, "")
	fmt.Println("请求时间 ", time.Now().Unix()-now, "     ", body)
}

func (this *JsonPostData) changePassword() {
	now := time.Now().Unix()
	url := host + "/game/user/change/password"
	info := make(map[string]string)
	info["account"] = "153630863@qq.com"
	info["password"] = "423522"
	info["new_password"] = "423522"
	fmt.Println(info)
	body := this.Http(url, info, 1, "")
	fmt.Println("请求时间 ", time.Now().Unix()-now, "     ", body)
}

func (this *JsonPostData) register() {
	now := time.Now().Unix()
	url := host + "/game/user/register"
	info := make(map[string]string)
	info["account"] = "153630865@qq.com"
	info["password"] = "423522"
	info["name"] = "aiai"
	info["number"] = "441781198712042240"
	info["question_a"] = "q1"
	info["answer_a"] = "a1"
	info["question_b"] = "q2"
	info["answer_b"] = "a2"
	fmt.Println(info)
	body := this.Http(url, info, 1, "")
	fmt.Println("请求时间 ", time.Now().Unix()-now, "     ", body)
}

func (this *JsonPostData) roleList() {
	now := time.Now().Unix()
	url := host + "/game/user/role/list?token=Az7BeN5Pgo4krVMczc2lqpYmKWZnL2Q9"
	info := make(map[string]string)
	//info["token"] = "Az7BeN5Pgo4krVMczc2lqpYmKWZnL2Q9"
	fmt.Println(info)
	body := this.Http(url, info, 1, "GET")
	fmt.Println("请求时间 ", time.Now().Unix()-now, "     ", body)
}

func (this *JsonPostData) roleCreate() {
	now := time.Now().Unix()
	url := host + "/game/user/role/create"
	info := make(map[string]string)
	info["token"] = "Az7BeN5Pgo4krVMczc2lqpYmKWZnL2Q9"
	info["career"] = "warrior"
	info["gender"] = "men"
	info["nickname"] = "你好1"
	fmt.Println(info)
	body := this.Http(url, info, 1, "POST")
	fmt.Println("请求时间 ", time.Now().Unix()-now, "     ", body)
}

func test_cache() {
	load := func(k cache.Key) (cache.Value, error) {
		//time.Sleep(100 * time.Millisecond) // Slow task
		fmt.Println("key=", k)
		return fmt.Sprintf("%d", k), nil
	}

	// Create a loading cache
	c := cache.NewLoadingCache(load,
		cache.WithMaximumSize(100),                 // Limit number of entries in the cache.
		cache.WithExpireAfterAccess(1*time.Minute), // Expire entries after 1 minute since last accessed.
		cache.WithRefreshAfterWrite(2*time.Minute), // Expire entries after 2 minutes since last created.
	)

	getTicker := time.Tick(100 * time.Millisecond)
	reportTicker := time.Tick(5 * time.Second)
	for {
		select {
		case <-getTicker:
			val, _ := c.Get(rand.Intn(200))
			fmt.Println(val)
		case <-reportTicker:
			st := cache.Stats{}
			c.Stats(&st)
			fmt.Printf("%+v\n", st)
		}
	}
}

func (this *JsonPostData) test() string {
	//println("test")
	return ""
}

var (
	hostenv       = "http://127.0.0.1:8080"
	hostgame      = "https://game.geekros.com"
	host          = ""
	http_token    = "YqXLemvpOz85Jxy02QV7qAxJ31YZnNW6LBDoedKzKkXeJ8YvdEMwjVP941pQ7r3Pc2bLgBOa6ox3RqWN52DyZmnA04jpaRwXz598MP0gyEO2kvmoBZ79aKAQDn6d4W3P"
	account_token = "8V5zg3746Z4N3p58850tN12HqbxHlIBYyJ942L12wDjd8a9L5JZy17Vjfo66BWE6"
	appid         = "n8Mui2t97knKt72V"
	appsecret     = "NJ77I3j7UHHtp7UueVeUptUO3VN0N1ee"
)
var env *string = flag.String("e", "1", "")

func main() {
	flag.Parse()
	println("env", *env)
	if *env == "1" {
		host = hostenv
	} else {
		host = hostgame
	}
	a := new(JsonPostData)
	a.test()
	//a.login()
	a.roleCreate()
	//a.roleList()

}
