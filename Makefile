generate:
	cd protos/src/ && python -m grpc_tools.protoc -I. --python_out=../../src/protos --grpc_python_out=../../src/protos *.proto
	find src/protos/ -type f -name "*.py" -print0 | xargs -0 sed -i '' -E 's,import server_pb2,from . import server_pb2, g'
	find src/protos/ -type f -name "*.py" -print0 | xargs -0 sed -i '' -E 's,import broadcast_pb2,from . import broadcast_pb2, g'
	find src/protos/ -type f -name "*.py" -print0 | xargs -0 sed -i '' -E 's,import physics_pb2,from . import physics_pb2, g'
	find src/protos/ -type f -name "*.py" -print0 | xargs -0 sed -i '' -E 's,import remote_pb2,from . import remote_pb2, g'
	find src/protos/ -type f -name "*.py" -print0 | xargs -0 sed -i '' -E 's,import health_pb2,from . import health_pb2, g'

