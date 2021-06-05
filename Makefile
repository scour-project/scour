all: clean install

install:
	python setup.py install

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
	python setup.py register
	python setup.py sdist upload

check: test flake8



test:
	python test_scour.py

test_version:
	PYTHONPATH=. python -m scour.scour --version

test_help:
	PYTHONPATH=. python -m scour.scour --help

flake8:
	flake8 --max-line-length=119

coverage:
	coverage run --source=scour test_scour.py
	coverage html
	coverage report
