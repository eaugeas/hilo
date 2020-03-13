MAKE=make

PROJECTS=hilo_rpc hilo_stage hilo_server hilo hilo_tool hilo_argparse
CHECKS=hilo_rpc/check hilo_stage/check hilo_server/check hilo/check hilo_tool/check hilo_argparse/check
CLEANS=hilo_rpc/clean hilo_stage/clean hilo_server/clean hilo/clean hilo_tool/clean hilo_argparse/clean
BUILDS=hilo_rpc/build hilo_stage/build hilo_server/build hilo/build hilo_tool/build hilo_argparse/build
TESTS=hilo_rpc/test hilo_stage/test hilo_server/test hilo/test hilo_tool/test hilo_argparse/test
DISTS=hilo_rpc/dist hilo_stage/dist hilo_server/dist hilo/dist hilo_tool/dist hilo_argparse/dist
MAKES=hilo_rpc

.PHONY: init build clean install test check

all: build

init: .venv

.venv:
	./scripts/init.sh

build: $(BUILDS)

%/build: %/Makefile
	$(MAKE) -C $(dir $<) build

install: $(DISTS)

%/dist: %/Makefile
	$(MAKE) -C $(dir $<) install

clean: $(CLEANS)

%/clean: %/Makefile
	$(MAKE) -C $(dir $<) clean

test: $(TESTS)

%/test: %/Makefile
	$(MAKE) -C $(dir $<) test

check: $(CHECKS)

%/check: %/Makefile
	$(MAKE) -C $(dir $<) check
