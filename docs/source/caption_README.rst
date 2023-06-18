..
   Comment in rst, two dots and three spaces
   use conf.py doc_string info

=====================
Documentation - Scour
=====================
Python 2.7 or 3.4+

Scour is an SVG (scalable vector graphics) optimizer/cleaner written in Python that reduces
the file size by optimizing the structure and removing unnecessary data.

.. note::
    It can be used to create streamlined vector graphics suitable
    for web deployment, publishing/sharing or further processing.

The goal of Scour is to output a file that:

* renders identically at a fraction of the size
* removes a lot of redundant information created by most SVG editors

Optimization options are typically lossless but can be tweaked for more aggressive cleaning.

Scour is open-source and licensed under 
`Apache License 2.0 <https://github.com/codedread/scour/blob/master/LICENSE>`_.

| Scour was originally developed by Jeff "codedread" Schiller and Louis Simard in 2010.
| The project moved to GitHub in 2013 an is now maintained by  Tobias "oberstet" Oberstein and Patrick "Ede_123" Storz.

Installation
~~~~~~~~~~~~

PyPI latest release `<https://pypi.python.org/pypi/scour>`_
::

    pip install scour


Trunk `latest version (.zip) <https://github.com/codedread/scour>`_ - ``might be broken!``
::

    pip install https://github.com/codedread/scour/archive/master.zip


Usage
~~~~~

Basic::

	scour -i input.svg -o output.svg


Basic *older versions of Internet Explorer*::

	scour -i input.svg -o output.svg --enable-viewboxing


Maximum scrubbing::

	scour -i input.svg -o output.svg --enable-viewboxing --enable-id-stripping \
	--enable-comment-stripping --shorten-ids --indent=none


Maximum scrubbing and a compressed SVGZ file::

	scour -i input.svg -o output.svgz --enable-viewboxing --enable-id-stripping \
	--enable-comment-stripping --shorten-ids --indent=none
