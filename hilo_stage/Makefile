PYTHON=python3
PIP=pip

build:
	$(PYTHON) setup.py build

clean:
	$(PYTHON) setup.py clean
	rm -rf build dist *.egg-info __pycache__

install:
	$(PIP) install -e .