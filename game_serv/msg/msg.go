package msg

import (
	"github.com/name5566/leaf/network/json"
)

// var Processor network.Processor
var Processor = json.NewProcessor()

func init() {
	Processor.Register(&Hello{})
}

type Hello struct {
	Name string
}
type HelloResp struct {
	Code int
	Msg  string
}
