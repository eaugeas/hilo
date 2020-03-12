MAKE=make

PROJECTS=hilo_rpc hilo_stage hilo_server hilo
BUILDS=hilo_rpc/build hilo_stage/build hilo_server/build hilo/build
DISTS=hilo_rpc/dist hilo_stage/dist hilo_server/dist hilo/dist
MAKES=hilo_rpc

.PHONY: init build clean install test

all: build

init: .venv

.venv: ./scripts/init.sh

build: $(BUILDS)

%/build: %/Makefile
	$(MAKE) -C $(dir $<) build

install: $(DISTS)

%/dist: %/Makefile
	$(MAKE) -C $(dir $<) install

clean:
	$(MAKE) -C hilo_rpc clean
	$(MAKE) -C hilo_stage clean
	$(MAKE) -C hilo_server clean
	$(MAKE) -C hilo clean

test:
	$(MAKE) -C hilo_rpc test
	$(MAKE) -C hilo_stage test
	$(MAKE) -C hilo_server test
	$(MAKE) -C hilo test
