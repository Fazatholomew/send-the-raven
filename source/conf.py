# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../send_the_raven"))


# -- Project information -----------------------------------------------------

project = "send-the-raven"
copyright = "2023, Jimmy Hikmatullah"
author = "Jimmy Hikmatullah"

# The full version, including alpha/beta/rc tags
release = "0.1.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx_favicon",
    "sphinx.ext.viewcode"
]
autosummary_generate = True
autodoc_typehints = "description"
autodoc_class_signature = "separated"
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_book_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {"show_toc_level": 2}

autosummary_methods = ["*"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pydantic": ("https://docs.pydantic.dev/2.3", None),
    "aiohttp": ("https://docs.aiohttp.org/en/latest", None),
    "asyncio": ("https://docs.python.org/3/", None),
    "geopy": ("https://geopy.readthedocs.io/en/stable/", None),
}

html_title = "Send The Raven"
html_logo = "_static/android-chrome-512x512.png"

favicons = [
    {"rel": "icon", "href": "favicon.ico", "type": "image/x-icon"},
    {"rel": "icon", "sizes": "16x16", "href": "favicon-16x16.png", "type": "image/png"},
    {"rel": "icon", "sizes": "32x32", "href": "favicon-32x32.png", "type": "image/png"},
    {
        "rel": "icon",
        "sizes": "192x192",
        "href": "favicon-192x192.png",
        "type": "image/png",
    },
    {
        "rel": "icon",
        "sizes": "512x512",
        "href": "favicon-512x512.png",
        "type": "image/png",
    },
    {"rel": "apple-touch-icon", "href": "apple-touch-icon.png", "type": "image/png"},
]
