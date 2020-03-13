MAKE=make

PROJECTS=hilo_rpc hilo_stage hilo_server hilo hilo_tool
CHECKS=$(patsubst %,%/check, $(PROJECTS))
CLEANS=$(patsubst %,%/clean, $(PROJECTS))
BUILDS=$(patsubst %,%/build, $(PROJECTS))
TESTS=$(patsubst %,%/test, $(PROJECTS))
DISTS=$(patsubst %,%/dist, $(PROJECTS))

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
