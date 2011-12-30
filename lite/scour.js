/**
 * Scour Lite (the JS version)
 *
 * Copyright(c) 2011 Google Inc.
 */

importScripts('pdom.js');

onmessage = function(evt) {
  // Now evt.data contains the text of the SVG file.
  postMessage({
    progress: {loaded: 100, total: 100},
    scouredSvg: scourString(evt.data)
  });
};

var NS = {
    'SVG': 		'http://www.w3.org/2000/svg', 
    'XLINK': 	'http://www.w3.org/1999/xlink', 
    'SODIPODI': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    'INKSCAPE': 'http://www.inkscape.org/namespaces/inkscape',
    'ADOBE_ILLUSTRATOR': 'http://ns.adobe.com/AdobeIllustrator/10.0/',
    'ADOBE_GRAPHS': 'http://ns.adobe.com/Graphs/1.0/',
    'ADOBE_SVG_VIEWER': 'http://ns.adobe.com/AdobeSVGViewerExtensions/3.0/',
    'ADOBE_VARIABLES': 'http://ns.adobe.com/Variables/1.0/',
    'ADOBE_SFW': 'http://ns.adobe.com/SaveForWeb/1.0/',
    'ADOBE_EXTENSIBILITY': 'http://ns.adobe.com/Extensibility/1.0/',
    'ADOBE_FLOWS': 'http://ns.adobe.com/Flows/1.0/',
    'ADOBE_IMAGE_REPLACEMENT': 'http://ns.adobe.com/ImageReplacement/1.0/',     
    'ADOBE_CUSTOM': 'http://ns.adobe.com/GenericCustomNamespace/1.0/',
    'ADOBE_XPATH': 'http://ns.adobe.com/XPath/1.0/'
};

var unwanted_ns = [ NS['SODIPODI'], NS['INKSCAPE'], NS['ADOBE_ILLUSTRATOR'],
    NS['ADOBE_GRAPHS'], NS['ADOBE_SVG_VIEWER'], NS['ADOBE_VARIABLES'],
    NS['ADOBE_SFW'], NS['ADOBE_EXTENSIBILITY'], NS['ADOBE_FLOWS'],
    NS['ADOBE_IMAGE_REPLACEMENT'], NS['ADOBE_CUSTOM'], NS['ADOBE_XPATH'] ];

/**
 * @param {pdom.Node|Node} node The parent node.
 * @param {Array.<string>} namespaces An array of namespace URIs.
 */
var removeNamespacedElements = function(node, namespaces) {
  if (node.nodeType == 1) {
    // Remove all namespace'd child nodes from this element.
    var childrenToRemove = [];
    for (var i = 0; i < node.childNodes.length; ++i) {
      var child = node.childNodes.item(i);
      if (namespaces.indexOf(child.namespaceURI) != -1) {
        childrenToRemove.push(child);
      }
    }
    
    for (var i = 0; i < childrenToRemove.length; ++i) {
      node.removeChild(childrenToRemove[i]);
    }
    
    // Now recurse for children.
    for (var i = 0; i < node.childNodes.length; ++i) {
      removeNamespacedElements(node.childNodes.item(i), namespaces);
    }
  }
};


/**
 * @param {string} in_string The SVG document as a string.
 * @param {object} opt_options An optional set of options.
 */
var scourString = function(in_string, opt_options) {
  postMessage({progress: {loaded: 0, total: 100}});

  var parser = new pdom.DOMParser();
  var options = opt_options || {};
  var doc = parser.parseFromString(in_string, 'text/xml');

  // Remove editor stuff.
  if (!options.keep_editor_data) {
    removeNamespacedElements(doc.documentElement, unwanted_ns);
    postMessage({message: 'Removed namespaced elements'});
  }

  return new pdom.XMLSerializer().serializeToString(doc);
};
