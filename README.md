# Scour
Scour is a Python module that takes an SVG file and produces a cleaner and more concise file. It is intended to be used after exporting with a GUI editor, such as Inkscape or Adobe Illustrator.

## Requirements
* [Python](https://www.python.org) 2.6 or later
* [six](https://pypi.python.org/pypi/six) 1.9 or later
* [psyco](https://pypi.python.org/pypi/psyco) (optional, Python 2.6 only)

## Installation
Scour can be installed manually or with a package manager, such as [pip](https://pip.pypa.io) or [Homebrew](http://brew.sh). It is also included as an Inkscape extension and in some Linux distributions.

### Manual installation
Download Scour and six and locate the `setup.py` file in both packages. Open a console and enter the following commands:
```
python /path/to/six/setup.py install
```
```
python /path/to/Scour/setup.py install
```
Do the same if you want to use psyco.

### Package manager
To install Scour using pip, enter the following command into a console:
```
pip install scour
```

To do the same with Homebrew:
```
brew install scour
```

Using pip or Homebrew will install six automatically (Homebrew will also install Python, if not installed).

## Usage
Standard:
```
scour -i input.svg -o output.svg
```
Better (for older versions of Internet Explorer):
```
scour -i input.svg -o output.svg --enable-viewboxing
```
Maximum scrubbing:
```
scour -i input.svg -o output.svg --enable-viewboxing --enable-id-stripping \
  --enable-comment-stripping --shorten-ids --indent=none
```
Maximum scrubbing and a compressed SVGZ file:
```
scour -i input.svg -o output.svgz --enable-viewboxing --enable-id-stripping \
  --enable-comment-stripping --shorten-ids --indent=none
```

## Licence
[Apache License 2.0](https://github.com/codedread/scour/blob/master/LICENSE)

## Development
Scour was originally developed by Jeff "codedread" Schiller and Louis Simard. Development is [now maintained](https://github.com/codedread/scour/issues/11) by Tobias "oberstet" Oberstein.

Scour was started as a vehicle for to learn Python. In addition, the goal was to reduce the amount of time spent in cleaning up files that are found on sites such as [openclipart.org](https://openclipart.org).

Ideas were pulled from three places:
  * the original author's head
  * Sam Ruby's [SVG Tidy script](http://intertwingly.net/code/svgtidy/svgtidy.rb)
  * Inkscape's [proposal for a 'cleaned SVG'](http://wiki.inkscape.org/wiki/index.php/Save_Cleaned_SVG)

This Github repository is the official one. The official website as well as older packages can be found at [www.codedread.com/scour](http://www.codedread.com/scour/).
