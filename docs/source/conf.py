#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# bluesky-adaptive documentation build configuration file, created by
# sphinx-quickstart on Thu Jun 28 12:35:56 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- General configuration ------------------------------------------------
import sphinx

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
    "matplotlib.sphinxext.plot_directive",
    "numpydoc",
    "sphinx_copybutton",
    "sphinx_design",
    "myst_parser",
]

# Configuration options for plot_directive. See:
# https://github.com/matplotlib/matplotlib/blob/f3ed922d935751e08494e5fb5311d3050a3b637b/lib/matplotlib/sphinxext/plot_directive.py#L81
plot_html_show_source_link = False
plot_html_show_formats = False

# Generate the API documentation when building
autosummary_generate = True
numpydoc_show_class_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "bluesky-adaptive"
copyright = "2020, NSLS-II"
author = "NSLS-II"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
import bluesky_adaptive

# The short X.Y version.
# version = bluesky_adaptive.__version__
# The full version, including alpha/beta/rc tags.
# release = bluesky_adaptive.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"
github_repo = project
github_user = "bluesky"

# Theme options for pydata_sphinx_theme
html_theme_options = dict(
    use_edit_page_button=True,
    github_url=f"https://github.com/{github_user}/{github_repo}",
    icon_links=[
        dict(
            name="PyPI",
            url=f"https://pypi.org/project/{project}",
            icon="fas fa-cube",
        ),
        dict(
            name="Community",
            url="https://blueskyproject.io/mattermost/",
            icon="fas fa-person-circle-question",
        ),
    ],
    external_links=[
        dict(
            name="Bluesky Project",
            url="https://blueskyproject.io",
        )
    ],
    show_toc_level=2,
    show_nav_level=1,
)

# A dictionary of values to pass into the template engine’s context for all pages
html_context = dict(
    github_user=github_user,
    github_repo=project,
    github_version="main",
    doc_path="docs/src",
)

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# This is a warning that causes failures, but the cross ref links are in tact.
suppress_warnings = ["myst.xref_missing"]

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "bluesky-adaptive"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "bluesky-adaptive.tex", "bluesky-adaptive Documentation", "Contributors", "manual"),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "bluesky-adaptive", "bluesky-adaptive Documentation", [author], 1)]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "bluesky-adaptive",
        "bluesky-adaptive Documentation",
        author,
        "bluesky-adaptive",
        "Tools for writing adaptive plans",
        "Miscellaneous",
    ),
]

default_role = "obj"


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable", None),
    "matplotlib": ("https://matplotlib.org", None),
    "bluesky": ("https://blueskyproject.io/bluesky/", None),
    "ophyd": ("https://blueskyproject.io/ophyd/", None),
    "event-model": ("https://blueskyproject.io/event-model/", None),
}

# nitpicky = sphinx.version_info >= (3,)
