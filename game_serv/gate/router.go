package gate

import (
	"serv/game"
	"serv/msg"
)

func init() {
	msg.Processor.SetRouter(&msg.Hello{}, game.ChanRPC)

}
