PYTHON=python3
PIP=pip
PYTEST=pytest
MYPY=mypy
FLAKE8=flake8

SRC=hilo_stage
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

check: typecheck lint-src lint-tests

typecheck:
	$(MYPY) --ignore-missing-imports

lint-src:
	$(FLAKE8) $(SRC)

lint-tests:
	$(FLAKE8) $(TESTS)

countlines:
	@echo $(SRC)	`find . -name '*.py' | xargs grep -E '\w' | wc -l`
