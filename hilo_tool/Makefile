PYTHON=python3
PIP=pip
PYTEST=pytest
MYPY=mypy
FLAKE8=flake8

SRC=hilo_tool_src
TESTS=tests

.PHONY: build clean install test check

all: check build

build:
	$(PYTHON) setup.py build

clean:
	$(PYTHON) setup.py clean
	rm -rf build dist *.egg-info __pycache__

install:
	$(PIP) install -e .

test:
	$(PYTEST) tests

check: typecheck-src typecheck-tests lint-src lint-tests

typecheck-src:
	$(MYPY) --ignore-missing-imports $(SRC)

typecheck-tests:
	$(MYPY) --ignore-missing-imports $(TESTS)

lint-src:
	$(FLAKE8) $(SRC)

lint-tests:
	$(FLAKE8) $(TESTS)
