# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))  # cesta do hlavného priečinka projektu
sys.path.insert(0, os.path.abspath('../../Implementation'))  # kde sú tvoje moduly
sys.path.insert(0, os.path.abspath('../../Implementation/data'))
sys.path.insert(0, os.path.abspath('../../Implementation/data/Model'))



# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Digital Twin of 5G Network'
copyright = '2025, David Truhlar'
author = 'David Truhlar'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'rst2pdf.pdfbuilder',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Add logo to the sidebar
html_logo = "_static/fiit_logo2.png"

# Optional: suppress logo at the top of the page (keep only in sidebar)
html_theme_options = {
    'logo_only': False,
}
