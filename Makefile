all: clean install

install:
	python setup.py install

clean:
	rm -rf build
	rm -rf dist
	rm -rf scour.egg-info

publish: clean
	python setup.py register
	python setup.py sdist upload

test_version:
	PYTHONPATH=. python -m scour.scour --version

test_help:
	PYTHONPATH=. python -m scour.scour --help
