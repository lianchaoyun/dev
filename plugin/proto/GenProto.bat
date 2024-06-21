cd C:\project\zhenzhen\loli
protoc --proto_path=./Proto/src  --csharp_out=../../loliclient/Assets/Script/Net/proto ./Proto/src/*.proto
protoc --proto_path=./Proto/src --go_out=../ ./Proto/src/*.proto
python3 gen_proto.py
pause