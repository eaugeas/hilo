PYTHON=python3
PIP=pip
PYTEST=pytest
MYPY=mypy
FLAKE8=flake8
YAPF=yapf
GRPCC=python -m grpc_tools.protoc

SRC=hilo_rpc
TESTS=tests
AUTOGEN=hilo_rpc/proto/source_pb2.py \
	hilo_rpc/proto/source_pb2_grpc.py \
	hilo_rpc/proto/sink_pb2.py \
	hilo_rpc/proto/sink_pb2_grpc.py \
	hilo_rpc/proto/pipeline_pb2.py \
	hilo_rpc/proto/stage_pb2.py \
	hilo_rpc/proto/connector_pb2.py \
	hilo_rpc/proto/metadata_pb2.py \
	hilo_rpc/proto/logging_pb2.py \
	hilo_rpc/proto/tests_pb2.py \
	hilo_rpc/proto/runner_pb2.py \
	hilo_rpc/proto/partition_pb2.py
TENSORFLOW_METADATA_AUTOGEN=tensorflow_metadata/proto/v0/path_pb2.py \
	tensorflow_metadata/proto/v0/schema_pb2.py \
	tensorflow_metadata/proto/v0/statistics_pb2.py

.PHONY: proto build clean install test check

all: build

build: proto
	$(PYTHON) setup.py build

install:
	$(PIP) install -e .

proto: $(AUTOGEN) $(TENSORFLOW_METADATA_AUTOGEN)

hilo_rpc/proto/%_pb2_grpc.py: hilo_rpc/proto/%_pb2.py
	@echo "GENERATING file from PROTOBUF "$@

hilo_rpc/proto/%_pb2.py: proto/hilo_rpc/proto/%.proto
	@echo "GENERATING file from PROTOBUF "$@
	@ $(GRPCC) \
		--proto_path proto \
		--grpc_python_out . \
		--python_out . \
		$<
tensorflow_metadata/proto/v0/%_pb2.py: proto/tensorflow_metadata/proto/v0/%.proto
	@echo "GENERATING file from PROTOBUF "$@
	@ $(GRPCC) \
		--proto_path proto \
		--python_out . \
		$<

clean:
	$(PYTHON) setup.py clean
	rm -rf build dist *.egg-info __pycache__
	@echo "CLEAN protobuf generated files"
	@ rm -f $(AUTOGEN) $(TENSORFLOW_METADATA_AUTOGEN)

test:
	$(PYTEST) tests

check: typecheck lint-src lint-tests

typecheck:
	$(MYPY) --ignore-missing-imports

lint-src:
	$(FLAKE8) --exclude *_pb2* $(SRC)

lint-tests:
	$(FLAKE8) $(TESTS)

countlines:
	@echo $(SRC)	`find . -name '*.py' -not -path "*hilo_rpc/proto*" | xargs grep -E '\w' | wc -l`

format-src:
	$(YAPF) -e hilo_rpc/proto -i -r $(SRC)

format-tests:
	$(YAPF) -i -r $(TESTS)

format: format-src format-tests
