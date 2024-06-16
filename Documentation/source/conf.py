import os
import sys
sys.path.insert(0, os.path.abspath('C:/Users/danie/Desktop/Dynamic Vision/DynamicVision/Modeling'))
sys.path.insert(0, os.path.abspath('C:/Users/danie/Desktop/Dynamic Vision/DynamicVision/GUI'))
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Dynamic Vision'
copyright = '2024, Daniel Philippi, Jens Rößler, Nicolas Scherer'
author = 'Daniel Philippi, Jens Rößler, Nicolas Scherer'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
