# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "ValidMind Developer Framework"
copyright = "2023, ValidMind Inc."
author = "ValidMind Inc."

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # Auto-generate documentation from docstrings
    "sphinx.ext.viewcode",  # Add links to source code
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    "sphinx_markdown_builder",  # Support for Markdown output
    "myst_parser",  # Support for Markdown
]

highlight_language = "python"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

autodoc_member_order = "bysource"
autosummary_generate = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
