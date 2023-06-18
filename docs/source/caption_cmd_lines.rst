Command line options
=====================

You can choose between different groups, categories.

.. note::
	An option starts with two minus signs.

Optimization
~~~~~~~~~~~~
.. list-table:: Optimization table
   :widths: 30 50
   :header-rows: 1

   * - Option
     - Description
   * - --set-precision
     - set number of significant digits (default: 5)
   * - --set-c-precision
     - set number of significant digits for control points, (default: same as '--set-precision')
   * - --disable-simplify-colors
     - won't convert colors to #RRGGBB format
   * - --disable-style-to-xml
     - won't convert styles into XML attributes
   * - --create-groups
     - create <g> elements for runs of elements with identical attributes
   * - --keep-editor-data
     - won't remove Inkscape, Sodipodi, Adobe Illustrator, "or Sketch elements and attributes
   * - --keep-unreferenced-defs
     - "won't remove elements within the defs container that are unreferenced
   * - --renderer-workaround
     - work around various renderer bugs (currently only librsvg) (default)
	 
Document
~~~~~~~~~
.. list-table:: Document options table
   :widths: 30 50
   :header-rows: 1

   * - Option
     - Description
   * - --strip-xml-prolog
     - won't output the XML prolog (<?xml ?>
   * - --remove-titles
     - remove <title> elements
   * - --remove-descriptions
     - remove <desc> elements
   * - --remove-metadata
     - remove <metadata> elements (which may contain license/author information etc.)
   * - --remove-descriptive-elements
     - remove <title>, <desc> and <metadata> elements
   * - --enable-comment-stripping
     - remove all comments (<!-- -->)
   * - --disable-embed-rasters
     - won't embed rasters as base64-encoded data
   * - --enable-viewboxing
     - changes document width/height to 100%/100% and creates viewbox coordinates
	 
Formatting
~~~~~~~~~~

.. list-table:: Formatting options table
   :widths: 30 50
   :header-rows: 1

   * - Option
     - Description
   * - --indent
     - indentation of the output: none, space, tab (default: 4)
   * - --nindent
     - depth of the indentation, i.e. number of spaces/tabs: (default: 4)
   * - --no-line-breaks
     - do not create line breaks in output; (also disables indentation; might be overridden by xml:space=\"preserve\"
   * - --strip-xml-space
     - strip the xml:space=\"preserve\" attribute from the root SVG element
	 
Id options
~~~~~~~~~~~

.. list-table:: Id options table
   :widths: 30 50
   :header-rows: 1

   * - Option
     - Description
   * - --enable-id-stripping
     - remove all unreferenced IDs
   * - --nindent
     - depth of the indentation, i.e. number of spaces/tabs: (default: 4)
   * - --shorten-ids
     - shorten all IDs to the least number of letters possible
   * - --shorten-ids-prefix
     - add custom prefix to shortened IDs
   * - --protect-ids-noninkscape
     - don't remove IDs not ending with a digit
   * - --protect-ids-list
     - don't remove IDs given in this comma-separated list
   * - --protect-ids-prefix
     - don't remove IDs starting with the given prefix
	 
Compatibility
~~~~~~~~~~~~~
.. list-table:: Compatibility options table
   :widths: 30 50
   :header-rows: 1

   * - Option
     - Description
   * - --error-on-flowtext
     - exit with error if the input SVG uses non-standard flowing text (only warn by default)


