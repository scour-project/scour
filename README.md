# Scour

**Build status:** [![Build Status](https://travis-ci.org/scour-project/scour.svg?branch=master)](https://travis-ci.org/scour-project/scour)

---

Scour is a Python tool that takes an SVG file and produces a cleaner and more concise file. It is intended to be used **after** exporting to SVG with a GUI editor, such as Inkscape or Adobe Illustrator.

Scour is open-source and licensed under [Apache License 2.0](https://github.com/codedread/scour/blob/master/LICENSE).

Scour was originally developed by Jeff "codedread" Schiller and Louis Simard. Development is [now maintained](https://github.com/codedread/scour/issues/11) by Tobias "oberstet" Oberstein.

This Github repository is the official one. The official website as well as older packages can be found at [www.codedread.com/scour](http://www.codedread.com/scour/).

## Installation

Scour requires [Python](https://www.python.org) 2.7 or 3.3+. Further, for installation, [pip](https://pip.pypa.io) should be used.

To install the [latest release](https://pypi.python.org/pypi/scour) of Scour from PyPI:

```console
pip install scour
```

To install the [latest trunk](https://github.com/codedread/scour) version (which might be broken!) from GitHub:

```console
pip install https://github.com/codedread/scour/archive/master.zip
```

## Usage

Standard:

```console
scour -i input.svg -o output.svg
```

Better (for older versions of Internet Explorer):

```console
scour -i input.svg -o output.svg --enable-viewboxing
```

Maximum scrubbing:

```console
scour -i input.svg -o output.svg --enable-viewboxing --enable-id-stripping \
  --enable-comment-stripping --shorten-ids --indent=none
```

Maximum scrubbing and a compressed SVGZ file:

```console
scour -i input.svg -o output.svgz --enable-viewboxing --enable-id-stripping \
  --enable-comment-stripping --shorten-ids --indent=none
```
