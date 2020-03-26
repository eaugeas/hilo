PYTHON=python3
PIP=pip
PYTEST=pytest
MYPY=mypy
FLAKE8=flake8
GRPCC=python -m grpc_tools.protoc
PROTOS=proto/*.proto
AUTOGEN=hilo_rpc/proto/source_pb2.py \
	hilo_rpc/proto/source_pb2_grpc.py \
	hilo_rpc/proto/sink_pb2.py \
	hilo_rpc/proto/sink_pb2_grpc.py \
	hilo_rpc/proto/pipeline_pb2.py \
	hilo_rpc/proto/stage_pb2.py \
	hilo_rpc/proto/storage_pb2.py \
	hilo_rpc/proto/metadata_pb2.py \
	hilo_rpc/proto/logging_pb2.py

SRC=hilo_rpc
TESTS=tests

.PHONY: proto build clean install test check

all: build

build: proto
	$(PYTHON) setup.py build

install:
	$(PIP) install -e .

proto: $(AUTOGEN)

hilo_rpc/proto/%_pb2_grpc.py: hilo_rpc/proto/%_pb2.py
	@echo "GENERATING file from PROTOBUF "$@

hilo_rpc/proto/%_pb2.py: proto/hilo_rpc/proto/%.proto
	@echo "GENERATING file from PROTOBUF "$@
	@ $(GRPCC) \
		--proto_path proto \
		--grpc_python_out . \
		--python_out . \
		$<

clean:
	$(PYTHON) setup.py clean
	rm -rf build dist *.egg-info __pycache__
	@echo "CLEAN protobuf generated files"
	@ rm -f $(AUTOGEN)

test:
	$(PYTEST) tests

check: typecheck lint-src lint-tests

typecheck:
	$(MYPY) --ignore-missing-imports

lint-src:
	$(FLAKE8) --exclude *_pb2* $(SRC)

lint-tests:
	$(FLAKE8) $(TESTS)
