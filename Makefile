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
	python setup.py bdist_egg upload
	python setup.py bdist_wininst upload
