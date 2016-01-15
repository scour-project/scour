# Scour

Scour is a Python tool that takes an SVG file and produces a cleaner and more concise file. It is intended to be used **after** exporting to SVG with a GUI editor, such as Inkscape or Adobe Illustrator.

Scour is open-source and licensed under [Apache License 2.0](https://github.com/codedread/scour/blob/master/LICENSE).

Scour was originally developed by Jeff "codedread" Schiller and Louis Simard. Development is [now maintained](https://github.com/codedread/scour/issues/11) by Tobias "oberstet" Oberstein.

This Github repository is the official one. The official website as well as older packages can be found at [www.codedread.com/scour](http://www.codedread.com/scour/).

## Installation

Scour requires [Python](https://www.python.org) 2.6 or 2.7 (Python 3 currently does NOT work - see [here](https://github.com/codedread/scour/issues/30)). Further, for installation, use [pip](https://pip.pypa.io):

```console
pip install scour
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
