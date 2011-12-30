/**
 * Pico DOM
 * Copyright(c) 2011, Google Inc.
 *
 * A really tiny implementation of the DOM for use in Web Workers.
 */

// TODO: Look into defineProperty instead of getters.

var pdom = pdom || {};

// ===========================================================================
// Stolen from Closure because it's the best way to do Java-like inheritance.
pdom.base = function(me, opt_methodName, var_args) {
  var caller = arguments.callee.caller;
  if (caller.superClass_) {
    // This is a constructor. Call the superclass constructor.
    return caller.superClass_.constructor.apply(
        me, Array.prototype.slice.call(arguments, 1));
  }

  var args = Array.prototype.slice.call(arguments, 2);
  var foundCaller = false;
  for (var ctor = me.constructor;
       ctor; ctor = ctor.superClass_ && ctor.superClass_.constructor) {
    if (ctor.prototype[opt_methodName] === caller) {
      foundCaller = true;
    } else if (foundCaller) {
      return ctor.prototype[opt_methodName].apply(me, args);
    }
  }

  // If we did not find the caller in the prototype chain,
  // then one of two things happened:
  // 1) The caller is an instance method.
  // 2) This method was not called by the right caller.
  if (me[opt_methodName] === caller) {
    return me.constructor.prototype[opt_methodName].apply(me, args);
  } else {
    throw Error(
        'goog.base called from a method of one name ' +
        'to a method of a different name');
  }
};
pdom.inherits = function(childCtor, parentCtor) {
  /** @constructor */
  function tempCtor() {};
  tempCtor.prototype = parentCtor.prototype;
  childCtor.superClass_ = parentCtor.prototype;
  childCtor.prototype = new tempCtor();
  childCtor.prototype.constructor = childCtor;
};
// ===========================================================================


/**
 * A DOMException
 *
 * @param {number} code The DOM exception code.
 * @constructor
 */
pdom.DOMException = function(code) {
  this.__defineGetter__('code', function() { return code });
};
pdom.DOMException.INDEX_SIZE_ERR                 = 1;
pdom.DOMException.DOMSTRING_SIZE_ERR             = 2;
pdom.DOMException.HIERARCHY_REQUEST_ERR          = 3;
pdom.DOMException.WRONG_DOCUMENT_ERR             = 4;
pdom.DOMException.INVALID_CHARACTER_ERR          = 5;
pdom.DOMException.NO_DATA_ALLOWED_ERR            = 6;
pdom.DOMException.NO_MODIFICATION_ALLOWED_ERR    = 7;
pdom.DOMException.NOT_FOUND_ERR                  = 8;
pdom.DOMException.NOT_SUPPORTED_ERR              = 9;
pdom.DOMException.INUSE_ATTRIBUTE_ERR            = 10;
pdom.DOMException.INVALID_STATE_ERR              = 11;
pdom.DOMException.SYNTAX_ERR                     = 12;
pdom.DOMException.INVALID_MODIFICATION_ERR       = 13;
pdom.DOMException.NAMESPACE_ERR                  = 14;
pdom.DOMException.INVALID_ACCESS_ERR             = 15;
pdom.DOMException.VALIDATION_ERR                 = 16;
pdom.DOMException.TYPE_MISMATCH_ERR              = 17;


/**
 * A NodeList.
 *
 * @param {Array.<Node>} nodeArray The array of nodes.
 * @constructor
 */
pdom.NodeList = function(nodeArray) {
  this.nodes_ = nodeArray;
  
  this.__defineGetter__('length', function() { return this.nodes_.length; });
};


/**
 * @param {number} index The index of the node to return.
 * @return {pdom.Node} The node.
 */
pdom.NodeList.prototype.item = function(index) {
  if (index >= 0 && index < this.length) {
    return this.nodes_[index];
  }
  return null;
};


/**
 * @param {Object.<string, pdom.Node>} nodeMap An object containing the
 *     attribute name-Node pairs.
 * @constructor
 */
pdom.NamedNodeMap = function(nodeMap) {
  this.setNodeMapInternal(nodeMap);
  this.__defineGetter__('length', function() { return this.attrs_.length });
};


/**
 * An array of the nodes.
 * @type {Array.<pdom.Node>}
 * @private
 */
pdom.NamedNodeMap.prototype.attrs_ = [];


/**
 * The node map.
 * @type {Object.<string, pdom.Node>}
 * @private
 */
pdom.NamedNodeMap.prototype.nodeMap_ = {};


/**
 * Sets the internal node map (and updates the array).
 * @param {Object.<string, pdom.Node>} The node map.
 */
pdom.NamedNodeMap.prototype.setNodeMapInternal = function(nodeMap) {
  this.nodeMap_ = {};
  this.attrs_ = [];
  for (var name in nodeMap) {
    var attr = new pdom.Attr(name, nodeMap[name]);
    this.attrs_.push(attr);
    this.nodeMap_[name] = attr;
  }
};


/**
 * @param {string} name The name of the node to return.
 * @return {pdom.Node} The named node.
 */
pdom.NamedNodeMap.prototype.getNamedItem = function(name) {
  return this.nodeMap_[name] || null;
};


/**
 * @param {number} index The index of the node to return.
 */
pdom.NamedNodeMap.prototype.item = function(index) {
  if (index >= 0 && index < this.attrs_.length) {
    return this.attrs_[index];
  }
  return null;
};


/**
 * A Node.
 *
 * @param {pdom.Node} opt_parentNode The parent node, which can be null.
 * @constructor
 */
pdom.Node = function(opt_parentNode) {
  this.parentNode_ = opt_parentNode;

  this.__defineGetter__('nodeType', function() { throw 'Unknown type of Node' });
  this.__defineGetter__('parentNode', function() { return this.parentNode_ });

  /**
   * An array of child nodes.
   * @type {Array.<pdom.Node>}
   * @private
   */
  this.childNodes_ = [];

  // Read-only properties.
  this.__defineGetter__('childNodes', function() {
    return new pdom.NodeList(this.childNodes_);
  });
  this.__defineGetter__('firstChild', function() {
    return this.childNodes_[0] || null;
  });
  this.__defineGetter__('lastChild', function() {
    return this.childNodes_.length <= 0 ? null :
        this.childNodes_[this.childNodes_.length - 1];
  });
  this.__defineGetter__('previousSibling', function() {
    var parent = this.parentNode;
    if (parent) {
      var familySize = parent.childNodes_.length;
      for (var i = 0; i < familySize; ++i) {
        var child = parent.childNodes_[i];
        if (child === this && i > 0) {
          return parent.childNodes_[i - 1];
        }
      }
    }
    return null;
  });
  this.__defineGetter__('nextSibling', function() {
    var parent = this.parentNode;
    if (parent) {
      var familySize = parent.childNodes_.length;
      for (var i = 0; i < familySize; ++i) {
        var child = parent.childNodes_[i];
        if (child === this && i < familySize - 1) {
          return parent.childNodes_[i + 1];
        }
      }
    }
    return null;
  });
  this.__defineGetter__('attributes', function() { return null });
  
  this.__defineGetter__('namespaceURI', function() {
    if (this.parentNode_) {
      return this.parentNode_.namespaceURI;
    }
    return null;
  });
};


pdom.Node.ELEMENT_NODE                   = 1;
pdom.Node.ATTRIBUTE_NODE                 = 2;
pdom.Node.TEXT_NODE                      = 3;
pdom.Node.CDATA_SECTION_NODE             = 4;
pdom.Node.ENTITY_REFERENCE_NODE          = 5;
pdom.Node.ENTITY_NODE                    = 6;
pdom.Node.PROCESSING_INSTRUCTION_NODE    = 7;
pdom.Node.COMMENT_NODE                   = 8;
pdom.Node.DOCUMENT_NODE                  = 9;
pdom.Node.DOCUMENT_TYPE_NODE             = 10;
pdom.Node.DOCUMENT_FRAGMENT_NODE         = 11;
pdom.Node.NOTATION_NODE                  = 12;


/**
 * @return {boolean} Whether the node has any children.
 */
pdom.Node.prototype.hasChildNodes = function() {
  return this.childNodes_.length > 0;
};


/**
 * @param {pdom.Node} child The node to remove.
 * @return {pdom.Node} The removed node.
 */
pdom.Node.prototype.removeChild = function(child) {
  var max = this.childNodes.length;
  for (var i = 0; i < max; ++i) {
    if (this.childNodes_[i] == child) {
      this.childNodes_.splice(i, 1);
      child.parentNode_ = null;
      return child;
    }
  }
  throw new pdom.DOMException(pdom.DOMException.NOT_FOUND_ERR);
};
 

/**
 * @param {pdom.Node} child The node to append.
 * @return {pdom.Node} The appended node.
 */
pdom.Node.prototype.appendChild = function(child) {
  if (child.parentNode) {
    child.parentNode.removeChild(child);
  }
  this.childNodes_.push(child);
  return child;
};


/**
 * A XML Document.
 *
 * @param {string} opt_text The optional text of the document.
 * @param {pdom.Node} opt_parentNode The parent node, which can be null.
 * @constructor
 * @extends {pdom.Node}
 */
pdom.XMLDocument = function(opt_text) {
  pdom.base(this, null);

  this.__defineGetter__('nodeType', function() {
    return pdom.Node.DOCUMENT_NODE;
  });
  this.__defineGetter__('documentElement', function() {
    for (var i = 0; i < this.childNodes_.length; ++i) {
      if (this.childNodes_[i].nodeType == 1) {
        return this.childNodes_[i];
      }
    }
    return null;
  });
};
pdom.inherits(pdom.XMLDocument, pdom.Node);


/**
 * A DocumentType node.
 *
 * @constructor
 * @extends {pdom.Node}
 */
pdom.DocumentType = function() {
  pdom.base(this, null);

  this.__defineGetter__('nodeType', function() {
    return pdom.Node.DOCUMENT_TYPE_NODE
  });
};
pdom.inherits(pdom.DocumentType, pdom.Node);


/**
 * An Attr node.
 *
 * @param {string} name The name of the attribute.
 * @param {string} value The value of the attribute.
 * @constructor
 * @extends {pdom.Attr}
 */
pdom.Attr = function(name, value) {
  pdom.base(this, null);
  
  this.__defineGetter__('nodeType', function() {
    return pdom.Node.ATTRIBUTE_NODE;
  });
  this.__defineGetter__('name', function() { return name });

  /**  
   * @type {string}
   */
  this.value = value;
};
pdom.inherits(pdom.Attr, pdom.Node);


/**
 * An Element node.
 *
 * @param {string} tagName The tag name of this element.
 * @param {pdom.Node} opt_parentNode The parent node, which can be null.
 * @param {Object.<string,string>} opt_attrs The attribute map.
 * @constructor
 * @extends {pdom.Node}
 */
pdom.Element = function(tagName, opt_parentNode, opt_attrs) {
  pdom.base(this, opt_parentNode);

  /**
   * Internal map of attributes for this element.
   *
   * @type {Object.<string, string>}
   * @private
   */
  this.attributes_ = opt_attrs || {};

  this.__defineGetter__('attributes', function() {
    if (!this.attributeMap_) {
      this.attributeMap_ = new pdom.NamedNodeMap(this.attributes_);
    }
    return this.attributeMap_;
  });
  
  this.__defineGetter__('nodeType', function() {
    return pdom.Node.ELEMENT_NODE;
  });
  this.__defineGetter__('tagName', function() { return tagName });
  this.__defineGetter__('nodeName', function() { return tagName });

  /**
   * @type {string}
   * @private
   */
  this.namespaceURI_ = this.parentNode_ ? this.parentNode_.namespaceURI : null;
  
  /**
   * Map of namespace prefix to URI.
   *
   * @type {Object.<string, string>}
   */
  this.nsPrefixMapInternal = {};
  
  // Generate map of prefixes to namespace URIs.  Also, discover if there is
  // a default namespace on this element.
  for (var attrName in this.attributes_) {
    if (attrName.indexOf('xmlns:') == 0 && attrName.length > 6) {
      var prefix = attrName.substring(6);
      this.nsPrefixMapInternal[prefix] = this.attributes_[attrName];
    } else if (attrName === 'xmlns') {
      this.namespaceURI_ = this.attributes_[attrName];
    }
  }

  // If the tagname includes a colon, resolve the namespace prefix.
  var colonIndex = tagName.indexOf(':');
  if (colonIndex != -1) {
    var prefix = tagName.substring(0, colonIndex);
    var node = this;
    while (node) {
      var uri = node.nsPrefixMapInternal[prefix];
      if (uri) {
        this.namespaceURI_ = uri;
        break;
      }
      node = node.parentNode;
    }
  }
  
  this.__defineGetter__('namespaceURI', function() { return this.namespaceURI_ });
};
pdom.inherits(pdom.Element, pdom.Node);


/**
 * @type {pdom.NamedNodeMap}
 * @private
 */
pdom.Element.prototype.attributeMap_ = null;


/**
 * @param {string} attrName The attribute name to get.
 */
pdom.Element.prototype.getAttribute = function(attrName) {
  var attrVal = this.attributes_[attrName] || '';
  return attrVal;
};


/**
 * @param {string} name The attribute name to set.
 * @param {string} value The attribute value to set.
 */
pdom.Element.prototype.setAttribute = function(name, value) {
  this.attributes_[name] = value;
  if (this.attributeMap_) {
    this.attributeMap_.setNodeMapInternal(this.attributes_);
  }
};


/**
 * @param {string} name The attribute to remove.
 */
pdom.Element.prototype.removeAttribute = function(name) {
  delete this.attributes_[name];
  if (this.attributeMap_) {
    this.attributeMap_.setNodeMapInternal(this.attributes_);
  }
};


/**
 * @return {boolean} Whether the element had an attribute.
 */
pdom.Element.prototype.hasAttribute = function(name) {
  return !!this.attributes_[name];
};


/**
 * CharacterData node.
 *
 * @param {string} opt_text The optional text of the document.
 * @param {pdom.Node} opt_parentNode The parent node, which can be null.
 * @constructor
 * @extends {pdom.Node}
 */
pdom.CharacterData = function(opt_text, opt_parentNode) {
  pdom.base(this, opt_parentNode);

  this.__defineGetter__('data', function() { return opt_text });
};
pdom.inherits(pdom.CharacterData, pdom.Node);


/**
 * A Comment node.
 *
 * @param {string} opt_text The optional text of the comment.
 * @param {pdom.Node} opt_parentNode The parent node, which can be null.
 * @constructor
 * @extends {pdom.CharacterData}
 */
pdom.Comment = function(opt_text, opt_parentNode) {
  pdom.base(this, opt_text);

  this.__defineGetter__('nodeType', function() {
    return pdom.Node.COMMENT_NODE;
  });
};
pdom.inherits(pdom.Comment, pdom.CharacterData);


/**
 * A Text node.
 *
 * @param {string} opt_text The optional text of the comment.
 * @param {pdom.Node} opt_parentNode The parent node, which can be null.
 * @constructor
 * @extends {pdom.CharacterData}
 */
pdom.Text = function(opt_text, opt_parentNode) {
  pdom.base(this, opt_text, opt_parentNode);

  this.__defineGetter__('nodeType', function() {
    return pdom.Node.TEXT_NODE;
  });
};
pdom.inherits(pdom.Text, pdom.CharacterData);



pdom.parse = {};

/**
 * Swallows all whitespace on the left.
 *
 * @private
 * @return {boolean} True if some whitespace characters were swallowed.
 */
pdom.parse.swallowWS_ = function(parsingContext) {
  var wsMatches = parsingContext.xmlText.match(/^\s+/);
  if (wsMatches && wsMatches.length > 0) {
    parsingContext.offset += wsMatches[0].length;
    return true;
  }
  return false;
};


/**
 * @private
 * @returns {boolean} True if some cruft was swallowed.
 */
pdom.parse.swallowXmlCruft_ = function(parsingContext, head, tail) {
  pdom.parse.swallowWS_(parsingContext);
  var text = parsingContext.xmlText;
  var start = parsingContext.offset;
  // If we find the start, strip it all off.
  if (text.indexOf(head, start) == 0) {
    var end = text.indexOf(tail, start + head.length);
    if (end == -1) {
      throw 'Could not find the end of the thing (' + tail + ')';
    }
    parsingContext.offset = end + tail.length;
    return true;
  }
  return false;
}


/**
 * Parses the XML prolog, if present.
 *
 * @private
 * @return {boolean} True if an XML prolog was found.
 */
pdom.parse.parseProlog_ = function(parsingContext) {
  return pdom.parse.swallowXmlCruft_(parsingContext, '<?xml ', '?>');
};


/**
 * Parses the DOCTYPE, if present.
 *
 * @return {boolean} True if a DOCTYPE was found.
 */
pdom.parse.parseDocType_ = function(parsingContext) {
  swallowWS(parsingContext);
  var text = parsingContext.xmlText;
  var start = parsingContext.offset;
  var head = '<!DOCTYPE ';
  if (text.indexOf(head, start) == 0) {
    // Deal with [] in the DOCTYPE.
    var startBracket = text.indexOf('[', start + head.length);
    if (startBracket != -1) {
      var endBracket = text.indexOf(']', startBracket + 1);
      if (endBracket == -1) {
        throw 'Could not find end ] in DOCTYPE';
      }
      start = endBracket + 1;
    }

    var endDocType = text.indexOf('>', start + head.length);
    if (endDocType == -1) {
      throw 'Could not find the end of the DOCTYPE (>)';
    }
    parsingContext.offset = endDocType + 2;
    return true;
  }
  return false;
};


/**
 * Parses one node from the XML stream.
 *
 * @private
 * @param {Object} parsingContext The parsing context.
 * @return {pdom.Node} Returns the Node or null if none are found.
 */
pdom.parse.parseOneNode_ = function(parsingContext) {
  var i = parsingContext.offset;
  var xmlText = parsingContext.xmlText;

  // Detect if it's a comment (<!-- -->)
  var COMMENT_START = '<!--';
  var COMMENT_END = '-->';
  if (xmlText.indexOf(COMMENT_START, i) == i) {
    var endComment = xmlText.indexOf(COMMENT_END, i + COMMENT_START.length + 1);
    if (endComment == -1) {
      throw "End tag for comment not found";
    }
    var newComment = new pdom.Comment(
        xmlText.substring(i + COMMENT_START.length, endComment),
        parsingContext.currentNode);
    parsingContext.currentNode.childNodes_.push(newComment);
    parsingContext.offset = endComment + COMMENT_END.length;
    return newComment;
  }

  // Determine if it's a DOCTYPE (<!DOCTYPE ...[]>)
  var DOCTYPE_START = '<!DOCTYPE ';
  var DOCTYPE_END = '>';
  if (xmlText.indexOf(DOCTYPE_START, i) == i) {
    // Deal with [] in the DOCTYPE.
    var startBracket = xmlText.indexOf('[', i + DOCTYPE_START.length + 1);
    if (startBracket != -1) {
      var endBracket = xmlText.indexOf(']', startBracket + 1);
      if (endBracket == -1) {
        throw 'Could not find end ] in DOCTYPE';
      }
      i = endBracket + 1;
    }

    // TODO: Is this right?  Shouldn't it be after the [] if they were present?
    var endDocType = xmlText.indexOf('>', i + DOCTYPE_START.length + 1);
    if (endDocType == -1) {
      throw 'Could not find the end of the DOCTYPE (>)';
    }
    var newDocType = new pdom.DocType();
    parsingContext.currentNode.childNodes_.push(newDocType);
    parsingContext.offset = endDocType + 1;
    return newDocType;
  }

  // If we are inside an element, see if we have the end tag.
  if (parsingContext.currentNode.nodeType == 1 &&
      xmlText.indexOf('</', i) == i) {
    // Look for end of end tag.
    var endEndTagIndex = xmlText.indexOf('>', i + 2);
    if (endEndTagIndex == -1) {
      throw 'Could not find end of end tag';
    }

    // Check if the tagname matches the end tag.  If not, that's an error.
    var tagName = xmlText.substring(i + 2, endEndTagIndex);
    if (tagName != parsingContext.currentNode.tagName) {
      throw 'Found </' + tagName + '> instead of </' +
          parsingContext.currentNode.tagName + '>';
    }
    
    // Otherwise, parsing of the current element is done.  Return it and
    // update the parsing context.
    var elementToReturn = parsingContext.currentNode;
    parsingContext.offset = endEndTagIndex + 1;
    parsingContext.currentNode = elementToReturn.parentNode;
    return elementToReturn;
  }

  // TODO: Detect if the element has a proper name.
  if (xmlText[i] == '<') {
    var isSelfClosing = false;
    var selfClosingElementIndex = xmlText.indexOf('/>', i + 1);
    var endStartTagIndex = xmlText.indexOf('>', i + 1)
    if (selfClosingElementIndex == -1 && endStartTagIndex == -1) {
      throw 'Could not find end of start tag in Element';
    }

    // Self-closing element.
    if (selfClosingElementIndex != -1 &&
        selfClosingElementIndex < endStartTagIndex) {
      endStartTagIndex = selfClosingElementIndex;
      isSelfClosing = true;
    }

    var attrs = {};

    // TODO: This should be whitespace, not space.
    var tagNameIndex = xmlText.indexOf(' ', i + 1);
    if (tagNameIndex == -1 || tagNameIndex > endStartTagIndex) {
      tagNameIndex = endStartTagIndex;
    } else {
      // Find all attributes and record them.
      var attrGlobs = xmlText.substring(tagNameIndex + 1, endStartTagIndex).trim();
      var j = 0;
      while (j < attrGlobs.length) {
        var equalsIndex = attrGlobs.indexOf('=', j);
        if (equalsIndex == -1) {
          break;
        }

        // Found an attribute name-value pair.
        var attrName = attrGlobs.substring(j, equalsIndex).trim();

        j = equalsIndex + 1;
        var theRest = attrGlobs.substring(j);
        var singleQuoteIndex = theRest.indexOf('\'', 0);
        var doubleQuoteIndex = theRest.indexOf('"', 0);
        if (singleQuoteIndex == -1 && doubleQuoteIndex == -1) {
          throw 'Attribute "' + attrName + '" found with no quoted value';
        }
        
        var quoteChar = '"';
        var quoteIndex = doubleQuoteIndex;
        if (singleQuoteIndex != -1 &&
            ((doubleQuoteIndex != -1 && singleQuoteIndex < doubleQuoteIndex) ||
            doubleQuoteIndex == -1)) {
          // Singly-quoted.
          quoteChar = '\'';
          quoteIndex = singleQuoteIndex;
        }
        
        var endQuoteIndex = theRest.indexOf(quoteChar, quoteIndex + 1);
        if (endQuoteIndex == -1) {
          throw 'Did not find end quote for value of attribute "' + attrName + '"';
        }
        
        var attrVal = theRest.substring(quoteIndex + 1, endQuoteIndex);
        attrs[attrName] = attrVal;
        
        j += endQuoteIndex + 1;
      }
    }
    
    var newElementNode = new pdom.Element(
        xmlText.substring(i + 1, tagNameIndex),
        parsingContext.currentNode,
        attrs);

    parsingContext.offset = endStartTagIndex + 1;
    parsingContext.currentNode.childNodes_.push(newElementNode);

    if (isSelfClosing) {
      // Nudge it past the closing bracket.
      parsingContext.offset += 1;
      return newElementNode;
    }

    // Else, recurse into this element.    
    parsingContext.currentNode = newElementNode;
    return pdom.parse.parseOneNode_(parsingContext);
  }

  // Everything else is a text node.
  if (i != xmlText.length) {
    var endTextIndex = xmlText.indexOf('<', i + 1);
    if (endTextIndex == -1) {
      endTextIndex = xmlText.length;
    }
    var theText = xmlText.substring(i, endTextIndex);
    var newTextNode = new pdom.Text(theText, parsingContext.currentNode);
    parsingContext.currentNode.childNodes_.push(newTextNode);
    parsingContext.offset = endTextIndex;
    return newTextNode;
  }
  
  return null;
};


/**
 * A DOM Parser.
 */
pdom.DOMParser = function(xmlText) {
};


/**
 *
 * @param {string} xmlText The XML Text.
 * @return {pdom.XMLDocument}
 */
pdom.DOMParser.prototype.parseFromString = function(xmlText) {
  var theDoc = new pdom.XMLDocument(xmlText);
  var parsingContext = {xmlText: xmlText, offset: 0, currentNode: theDoc};
  pdom.parse.parseProlog_(parsingContext);
  while (!!(node = pdom.parse.parseOneNode_(parsingContext))) {
    // do nothing.
  };
  return theDoc;
};


/**
 * A XML Serializer.
 */
pdom.XMLSerializer = function() {
};


/**
 * @param {pdom.Node} node A node.
 * @return {string} The node serialized to text.
 */
pdom.XMLSerializer.prototype.serializeToString = function(node) {
  if (!(node instanceof pdom.Node)) {
    throw 'Argument XMLSerializer.serializeToString() was not a pdom.Node';
  }
  var str = '';
  switch (node.nodeType) {
    case pdom.Node.DOCUMENT_NODE:
      return this.serializeToString(node.documentElement);
    case pdom.Node.ELEMENT_NODE: 
      str = '<' + node.tagName;
      if (node.attributes && node.attributes.length > 0) {
        for (var i = 0; i < node.attributes.length; ++i) {
          var attr = node.attributes.item(i);
          str += ' ' + attr.name + '="' + attr.value + '"';
        }
      }
      if (node.childNodes.length > 0) {
        str += '>';
        for (var i = 0; i < node.childNodes.length; ++i) {
          var child = node.childNodes.item(i);
          str += this.serializeToString(child);
        }
        str += '</' + node.tagName + '>';
      } else {
        str += '/>'
      }
      return str;
    case pdom.Node.TEXT_NODE:
      return node.data;
  }
};
