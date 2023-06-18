"""Configuration file for the Sphinx documentation builder.
::

    # !!! indentation of sphinx is 3 leading spaces for index.rts, code has :: \n and 4 spaces like this
    # https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
    pip install -U sphinx
    pip install sphinx-rtd-theme
    pip install sphinxcontrib-napoleon
    # Use sphinx-apidoc to build your API documentation:
    cd docs
    sphinx-apidoc -f -o source/ ../scour/
    make html
    # if you add a rst document, add to index.rst and rerun sphinx-apidoc -f -o source/ ../scour/
    #
    # create a page, web hook, on readthedocs.org and update manually on docu change

"""
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# Project information footer of website
project = "scour"
copyright = "Apache 2.0, Jeff Schiller, Louis Simard, Tavendo GmbH"
author = "44xtc44"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add napoleon to the extensions list; parse NumPy and Google style docstrings
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel'
]


# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
pygments_style = 'sphinx'

html_static_path = ['static']
html_logo = "./static/scour.png"
html_logo_only = True
html_display_version = False
html_css_files = ["css-style.css"]
