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

test_error_on_flowtext:
	# this is fine ..
	PYTHONPATH=. scour --error-on-flowtext unittests/flowtext-less.svg /dev/null
	# .. and this should bail out!
	PYTHONPATH=. scour --error-on-flowtext unittests/flowtext.svg /dev/null

flake8:
	flake8 --max-line-length=119