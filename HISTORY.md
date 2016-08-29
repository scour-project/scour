# Release Notes for Scour

## Version 0.35 (not released yet)

* Add `--order-attributes` option which orders attributes alphabetically in output. ([#59](https://github.com/scour-project/scour/issues/59))
* Drop official support for Python 2.6. (While it will probably continue to work for a while compatibility is not guaranteed anymore. If you continue to use Scour with Python 2.6 and should find/fix any compatibility issues pull requests are welcome, though.)
* Fix: Unused IDs were not shortended when `--shorten-ids` was used.
* Fix: Most elements were still removed from `<defs>` when `--keep-unreferenced-defs` was used. ([#62](https://github.com/scour-project/scour/issues/62))
* Improve escaping of single/double quotes ('/") in attributes. ([#64](https://github.com/scour-project/scour/issues/64))
* Print usage information if no input file was specified (and no data is available from `stdin`).([#65](https://github.com/scour-project/scour/issues/65))
* Redirect informational output to `stderr` when SVG is output to `stdout`. ([#67](https://github.com/scour-project/scour/issues/67))
* Allow elements to be found via `Document.getElementById()` in the minidom document returned by scourXmlFile(). ([#68](https://github.com/scour-project/scour/issues/68))
* Improve code to remove default attribute values and add a lot of new default values. ([#70](https://github.com/scour-project/scour/issues/70))
* Fix: Only attempt to group elements that the content model allows to be children of a `<g>` when `--create-groups` is specified. (#98)
* Fix: Update list of SVG presentation attributes allowing more styles to be converted to attributes and remove two entries (`line-height` and `visibility`) that were actually invalid. (#99)


## Version 0.34 (2016-07-25)

* Add a function to sanitize an arbitrary Python object containing options for Scour as attributes (usage: `Scour.sanitizeOptions(options)`).<br>This simplifies usage of the Scour module by other scripts while avoiding any compatibility issues that might arise when options are added/removed/renamed in Scour. ([#44](https://github.com/scour-project/scour/issues/44))
* Input/output file can now be specified as positional arguments (e.g. `scour input.svg output.svg`). ([#46](https://github.com/scour-project/scour/issues/46))
* Improve `--help` output by intuitively arranging options in groups. ([#46](https://github.com/scour-project/scour/issues/46))
* Add option `--error-on-flowtext` to raise an exception whenever a non-standard `<flowText>` element is found (which is only supported in Inkscape). If this option is not specified a warning will be shown. ([#53](https://github.com/scour-project/scour/issues/53))
* Automate tests with continouous integration via Travis. ([#52](https://github.com/scour-project/scour/issues/52))


## Version 0.33 (2016-01-29)

* Add support for removal of editor data of Sketch. ([#37](https://github.com/scour-project/scour/issues/37))
* Add option `--verbose` (or `-v`) to show detailed statistics after running Scour. By default only a single line containing the most important information is output now.


## Version 0.32 (2015-12-10)

* Add functionality to remove unused XML namespace declarations from the `<svg>` root element. ([#14](https://github.com/scour-project/scour/issues/14))
* Restore unittests which were lost during move to GitHub. ([#24](https://github.com/scour-project/scour/issues/24))
* Fix a potential regex matching issue in `points` attribute of `<polygon>` and `<polyline>` elements. ([#24](https://github.com/scour-project/scour/issues/24))
* Fix a crash with `points` attribute of `<polygon>` and `<polyline>` starting with a negative number. ([#24](https://github.com/scour-project/scour/issues/24))
* Fix encoding issues when input file contained unicode characters. ([#27](https://github.com/scour-project/scour/issues/27))
* Fix encoding issues when using `stding`/`stdout` as input/output.  ([#27](https://github.com/scour-project/scour/issues/27))
* Fix removal of comments. If a node contained multiple comments usually not all of them were removed. ([#28](https://github.com/scour-project/scour/issues/28))


## Version 0.31 (2015-11-16)

* Ensure Python 3 compatibility. ([#8](https://github.com/scour-project/scour/issues/8))
* Add option `--nindent` to set the number of spaces/tabs used for indentation (defaults to 1). ([#13](https://github.com/scour-project/scour/issues/13))
* Add option `--no-line-breaks` to suppress output of line breaks and indentation altogether. ([#13](https://github.com/scour-project/scour/issues/13))
* Add option `--strip-xml-space` which removes the specification of `xml:space="preserve"` on the `<svg>` root element which would otherwise disallow Scour to make any whitespace changes in output. ([#13](https://github.com/scour-project/scour/issues/13))


## Version 0.30 (2014-08-05)

* Fix ingoring of additional args when invoked from scons.


## Version 0.29 (2014-07-26)

* Add option `--keep-unreferenced-defs` to preserve elements in `<defs>` that are not referenced and would be removed otherwise. ([#2](https://github.com/scour-project/scour/issues/2))
* Add option to ingore unknown cmd line opts.


## Version 0.28 (2014-01-12)

* Add option `--shorten-ids-prefix` which allows to add a custom prefix to all shortened IDs. ([#1](https://github.com/scour-project/scour/issues/1))


## Version 0.27 (2013-10-26)

* Allow direct calling of the Scour module.


## Version 0.26 (2013-10-22)

* Re-release of Scour 0.26, re-packaged as a Python module [available from PyPI](https://pypi.python.org/pypi/scour) (Thanks to [Tobias Oberstet](https://github.com/oberstet)!).
* Development moved to GitHub (https://github.com/scour-project/scour).


## Version 0.26 (2011-05-09)

* Fix [Bug 702423](https://bugs.launchpad.net/scour/+bug/702423) to function well in the presence of multiple identical gradients and `--disable-style-to-xml`.
* Fix [Bug 722544](https://bugs.launchpad.net/scour/+bug/722544) to properly optimize transformation matrices. Also optimize more things away in transformation specifications. (Thanks to Johan Sundstr&ouml;m for the patch.)
* Fix [Bug 616150](https://bugs.launchpad.net/scour/+bug/616150) to run faster using the `--create-groups` option.
* Fix [Bug 708515](https://bugs.launchpad.net/scour/+bug/562784) to handle raster embedding better in the presence of file:// URLs.
* Fix [Bug 714717](https://bugs.launchpad.net/scour/+bug/714717) to avoid deleting renderable CurveTo commands in paths, which happen to end where they started.
* Per [Bug 714727](https://bugs.launchpad.net/scour/+bug/714727) and [Bug 714720](https://bugs.launchpad.net/scour/+bug/714720), Scour now deletes text attributes, including "text-align", from elements and groups of elements that only contain shapes. (Thanks to Jan Thor for the patches.)
* Per [Bug 714731](https://bugs.launchpad.net/scour/+bug/714731), remove the default value of more SVG attributes. (Thanks to Jan Thor for the patch.)
* Fix [Bug 717826](https://bugs.launchpad.net/scour/+bug/717826) to emit the correct line terminator (CR LF) in optimized SVG content on the version of Scour used in Inkscape on Windows.
* Fix [Bug 734933](https://bugs.launchpad.net/scour/+bug/734933) to avoid deleting renderable LineTo commands in paths, which happen to end where they started, if their stroke-linecap property has the value "round".
* Fix [Bug 717254](https://bugs.launchpad.net/scour/+bug/717254) to delete `<defs>` elements that become empty after unreferenced element removal. (Thanks to Jan Thor for the patch.)
* Fix [Bug 627372](https://bugs.launchpad.net/scour/+bug/627372) to future-proof the parameter passing between Scour and Inkscape. (Thanks to Bernd Feige for the patch.)
* Fix [Bug 638764](https://bugs.launchpad.net/scour/+bug/638764), which crashed Scour due to [Python Issue 2531](http://bugs.python.org/issue2531) regarding floating-point handling in ArcTo path commands. (Thanks to [Walther](https://launchpad.net/~walther-md) for investigating this bug.)
* Per [Bug 654759](https://bugs.launchpad.net/scour/+bug/654759), enable librsvg workarounds by default in Scour.
* Added ID change and removal protection options per [bug 492277](https://bugs.launchpad.net/scour/+bug/492277): `--protect-ids-noninkscape`, `--protect-ids-prefix`, `--protect-ids-list`. (Thanks to Jan Thor for this patch.)


## Version 0.25 (2010-07-11)

* Fix [Bug 541889](https://bugs.launchpad.net/scour/+bug/541889) to parse polygon/polyline points missing whitespace/comma separating a negative value.  Always output points attributes as comma-separated.
* Fix [Bug 519698](https://bugs.launchpad.net/scour/+bug/519698) to properly parse move commands that have line segments.
* Fix [Bug 577940](https://bugs.launchpad.net/scour/+bug/577940) to include stroke-dasharray into list of style properties turned into XML attributes.
* Fix [Bug 562784](https://bugs.launchpad.net/scour/+bug/562784), typo in Inkscape description
* Fix [Bug 603988](https://bugs.launchpad.net/scour/+bug/603988), do not commonize attributes if the element is referenced elsewhere.
* Fix [Bug 604000](https://bugs.launchpad.net/scour/+bug/604000), correctly remove default overflow attributes.
* Fix [Bug 603994](https://bugs.launchpad.net/scour/+bug/603994), fix parsing of `<style>` element contents when a CDATA is present
* Fix [Bug 583758](https://bugs.launchpad.net/scour/+bug/583758), added a bit to the Inkscape help text saying that groups aren't collapsed if IDs are also not stripped.
* Fix [Bug 583458](https://bugs.launchpad.net/scour/+bug/583458), another typo in the Inkscape help tab.
* Fix [Bug 594930](https://bugs.launchpad.net/scour/+bug/594930),  In a `<switch>`, require one level of `<g>` if there was a `<g>` in the file already. Otherwise, only the first subelement of the `<g>` is chosen and rendered.
* Fix [Bug 576958](https://bugs.launchpad.net/scour/+bug/576958), "Viewbox option doesn't work when units are set", when renderer workarounds are disabled.
* Added many options: `--remove-metadata`, `--quiet`, `--enable-comment-stripping`, `--shorten-ids`, `--renderer-workaround`.


## Version 0.24 (2010-02-05)

* Fix [Bug 517064](https://bugs.launchpad.net/scour/+bug/517064) to make XML well-formed again
* Fix [Bug 503750](https://bugs.launchpad.net/scour/+bug/503750) fix Inkscape extension to correctly pass `--enable-viewboxing`
* Fix [Bug 511186](https://bugs.launchpad.net/scour/+bug/511186) to allow comments outside of the root `<svg>` node


## Version 0.23 (2010-01-04)

* Fix [Bug 482215](https://bugs.launchpad.net/scour/+bug/482215) by using os.linesep to end lines
* Fix unittests to run properly in Windows
* Removed default scaling of image to 100%/100% and creating a viewBox.  Added `--enable-viewboxing` option to explicitly turn that on
* Fix [Bug 503034](https://bugs.launchpad.net/scour/+bug/503034) by only removing children of a group if the group itself has not been referenced anywhere else in the file


## Version 0.22 (2009-11-09)

* Fix [Bug 449803](https://bugs.launchpad.net/scour/+bug/449803) by ensuring input and output filenames differ.
* Fix [Bug 453737](https://bugs.launchpad.net/scour/+bug/453737) by updated Inkscape's scour extension with a UI
* Fix whitespace collapsing on non-textual elements that had xml:space="preserve"
* Fix [Bug 479669](https://bugs.launchpad.net/scour/+bug/479669) to handle empty `<style>` elements.


## Version 0.21 (2009-09-27)

* Fix [Bug 427309](https://bugs.launchpad.net/scour/+bug/427309) by updated Scour inkscape extension file to include yocto_css.py
* Fix [Bug 435689](https://bugs.launchpad.net/scour/+bug/435689) by properly preserving whitespace in XML serialization
* Fix [Bug 436569](https://bugs.launchpad.net/scour/+bug/436569) by getting `xlink:href` prefix correct with invalid SVG


## Version 0.20 (2009-08-31)

* Fix [Bug 368716](https://bugs.launchpad.net/scour/+bug/368716) by implementing a really tiny CSS parser to find out if any style element have rules referencing gradients, filters, etc
* Remove unused attributes from parent elements
* Fix a bug with polygon/polyline point parsing if there was whitespace at the end


## Version 0.19 (2009-08-13)

* Fix XML serialization bug: `xmlns:XXX` prefixes not preserved when not in default namespace
* Fix XML serialization bug: remapping to default namespace was not actually removing the old prefix
* Move common attributes to ancestor elements
* Fix [Bug 412754](https://bugs.launchpad.net/scour/+bug/401628): Elliptical arc commands must have comma/whitespace separating the coordinates
* Scour lengths for svg x,y,width,height,*opacity,stroke-width,stroke-miterlimit


## Version 0.18 (2009-08-09)

* Remove attributes of gradients if they contain default values
* Reduce bezier/quadratic (c/q) segments to their shorthand equivalents (s/t)
* Move to a custom XML serialization such that `id`/`xml:id` is printed first (Thanks to Richard Hutch for the suggestion)
* Added `--indent` option to specify indentation type (default='space', other options: 'none', 'tab')


## Version 0.17 (2009-08-03)

* Only convert to #RRGGBB format if the color name will actually be shorter
* Remove duplicate gradients
* Remove empty q,a path segments
* Scour polyline coordinates just like path/polygon
* Scour lengths from most attributes
* Remove redundant SVG namespace declarations and prefixes


## Version 0.16 (2009-07-30)

* Fix [Bug 401628](https://bugs.launchpad.net/scour/+bug/401628): Keep namespace declarations when using `--keep-editor-data` (Thanks YoNoSoyTu!)
* Remove trailing zeros after decimal places for all path coordinates
* Use scientific notation in path coordinates if that representation is shorter
* Scour polygon coordinates just like path coordinates
* Add XML prolog to scour output to ensure valid XML, added `--strip-xml-prolog` option


## Version 0.15 (2009-07-05)

* added `--keep-editor-data` command-line option
* Fix [Bug 395645](https://bugs.launchpad.net/scour/+bug/395645): Keep all identified children inside a defs (Thanks Frederik!)
* Fix [Bug 395647](https://bugs.launchpad.net/scour/+bug/395647): Do not remove closepath (Z) path segments


## Version 0.14 (2009-06-10)

* Collapse adjacent commands of the same type
* Convert straight curves into line commands
* Eliminate last segment in a polygon
* Rework command-line argument parsing
* Fix bug in embedRasters() caused by new command-line parsing
* added `--disable-embed-rasters` command-line option


## Version 0.13 (2009-05-19)

* properly deal with `fill="url(&quot;#foo&quot;)"`
* properly handle paths with more than 1 pair of coordinates in the first Move command
* remove font/text styles from shape elements (font-weight, font-size, line-height, etc)
* remove -inkscape-font-specification styles
* added `--set-precision` argument to set the number of significant digits (defaults to 5 now)
* collapse consecutive h,v coords/segments that go in the same direction


## Version 0.12 (2009-05-17)

* upgraded enthought's path parser to handle scientific notation in path coordinates
* convert colors to #RRGGBB format
* added option to disable color conversion


## Version 0.11 (2009-04-28)

* convert gradient stop offsets from percentages to float
* convert gradient stop offsets to integers if possible (0 or 1)
* fix bug in line-to-hv conversion
* handle non-ASCII characters (Unicode)
* remove empty line or curve segments from path
* added option to prevent style-to-xml conversion
* handle compressed svg (svgz) on the input and output
* added total time taken to the report
* Removed XML pretty printing because of [this problem](http://ronrothman.com/public/leftbraned/xml-dom-minidom-toprettyxml-and-silly-whitespace/).


## Version 0.10 (2009-04-27)

* Remove path with empty d attributes
* Sanitize path data (remove unnecessary whitespace)
* Convert from absolute to relative path data
* Remove trailing zeroes from path data
* Limit to no more than 6 digits of precision
* Remove empty line segments
* Convert lines to horiz/vertical line segments where possible
* Remove some more default styles (`display:none`, `visibility:visible`, `overflow:visible`,
          `marker:none`)


## Version 0.09 (2009-04-25)

* Fix bug when removing stroke styles
* Remove gradients that are only referenced by one other gradient
* Added option to prevent group collapsing
* Prevent groups with title/desc children from being collapsed
* Remove stroke="none"


## Version 0.08 (2009-04-22)

* Remove unnecessary nested `<g>` elements
* Remove duplicate gradient stops (same offset, stop-color, stop-opacity)
* Always keep fonts inside `<defs>`, always keep ids on fonts
* made ID stripping optional (disabled by default)


## Version 0.07 (2009-04-15)

* moved all functionality into a module level function named 'scour' and began adding unit tests
* prevent metadata from being removed if they contain only text nodes
* Remove unreferenced pattern and gradient elements outside of defs
* Removal of extra whitespace, pretty printing of XML


## Version 0.06 (2009-04-13)

* Prevent error when stroke-width property value has a unit
* Convert width/height into a viewBox where possible
* Convert all referenced rasters into base64 encoded URLs if the files can be found


## Version 0.05 (2009-04-07)

* Removes unreferenced elements in a `<defs>`
* Removes all inkscape, sodipodi, adobe elements
* Removes all inkscape, sodipodi, adobe attributes
* Remove all unused namespace declarations on the document element
* Removes any empty `<defs>`, `<metadata>`, or `<g>` elements
* Style fix-ups:
* Fixes any style properties like this: `style="fill: url(#linearGradient1000) rgb(0, 0, 0);"`
   * Removes any style property of: `opacity: 1;`
   * Removes any stroke properties when `stroke=none` or `stroke-opacity=0` or `stroke-width=0`
   * Removes any fill properties when `fill=none` or `fill-opacity=0`
   * Removes all fill/stroke properties when `opacity=0`
   * Removes any `stop-opacity: 1`
   * Removes any `fill-opacity: 1`
   * Removes any `stroke-opacity: 1`
* Convert style properties into SVG attributes
