# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

# -- Project information -----------------------------------------------------

project = 'QWAK'
copyright = '2022, Jaime Santos, Bruno Chagas, Rodrigo Chaves, Lorenzo Buffoni'
author = 'Jaime Santos, Bruno Chagas, Rodrigo Chaves, Lorenzo Buffoni'

# The full version, including alpha/beta/rc tags
release = '06/04/2022'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
]

autodoc_member_order = 'bysource'
autoclass_content = 'both'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "sphinx_rtd_theme"
# html_theme_options = {
#         'navbar_fixed_top': "true",
#         'source_link_position': "footer",
#         'globaltoc_depth': -1,
#         'bootstrap_version': "3",
#         #'bootswatch_theme': "united",
#         #'bootswatch_theme': "lumen",
#         # 'bootswatch_theme': "Darkly",
#         'navbar_links': [("Index", "genindex"),
#             ("Source","https://github.com/JaimePSantos/QWAK",True)],
#         'navbar_pagenav': False,
#         'nosidebar': False,
#     }

# html_sidebars = {
#     '**': [
#         'globaltoc.html',
#         'localtoc.html',
#     ]
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

add_function_parentheses = True

add_module_names = False

pygments_style = 'sphinx'

html_short_title = 'QWAK'

autodoc_typehints = "both"
