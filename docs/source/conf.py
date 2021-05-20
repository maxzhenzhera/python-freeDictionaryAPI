# -- Path setup --------------------------------------------------------------

import os
import sys

from pip._vendor.pkg_resources import parse_version


sys.path.insert(0, os.path.abspath('../..'))


import freedictionaryapi


# -- Project information -----------------------------------------------------

project = 'python-FreeDictionaryApi'
copyright = '2021, Max Zhenzhera'
author = 'Max Zhenzhera'


parsed_version = parse_version(freedictionaryapi.__version__)

# The short X.Y version.
version = parsed_version.base_version

# The full version, including alpha/beta/rc tags.
release = freedictionaryapi.__version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',  # Core library for html generation from docstrings
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',  # Create neat summary tables
]
autosummary_generate = True  # Turn on sphinx.ext.autosummary

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']