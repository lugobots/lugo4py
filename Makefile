generate:
	cd protos/src/ && python -m grpc_tools.protoc -I. --python_out=../../src/gen --grpc_python_out=../../src/gen *.proto

