all: clean install

install:
	python3 setup.py install

clean:
	rm -rf build
	rm -rf dist
	rm -rf scour.egg-info
	rm -rf .tox
	rm -f .coverage*
	rm -rf htmlcov
	find . -name "*.pyc" -type f -exec rm -f {} \;
	find . -name "*__pycache__" -type d -prune -exec rm -rf {} \;

publish: clean
	python3 setup.py register
	python3 setup.py sdist upload

check: test flake8



test:
	python3 test_scour.py

test_version:
	PYTHONPATH=. python3 -m scour.scour --version

test_help:
	PYTHONPATH=. python3 -m scour.scour --help

flake8:
	flake8 --max-line-length=119

coverage:
	coverage run --source=scour test_scour.py
	coverage html
	coverage report
