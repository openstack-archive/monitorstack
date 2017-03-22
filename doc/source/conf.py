#!/usr/bin/env python3

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import openstackdocstheme
import pbr.version
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'oslosphinx',
    'sphinxmark'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'monitorstack'
copyright = u'2017, OpenStack-Ansible Contributors'
author = u'OpenStack-Ansible Contributors'

# The link to the browsable source code (for the left hand menu)
oslosphinx_cgit_link = ('http://git.openstack.org/cgit/openstack'
                        '/{0}'.format(project))

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version_info = pbr.version.VersionInfo(project)
# The full version, including alpha/beta/rc tags.
release = version_info.version_string_with_vcs()
# The short X.Y version.
version = version_info.canonical_version_string()

# A few variables have to be set for the log-a-bug feature.
#   giturl: The location of conf.py on Git. Must be set manually.
#   gitsha: The SHA checksum of the bug description.
#           Automatically extracted from git log.
#   bug_tag: Tag for categorizing the bug. Must be set manually.
# These variables are passed to the logabug code via html_context.
giturl = ("http://git.openstack.org/cgit/openstack/{0}"
          "/tree/doc/source").format(project)
git_cmd = "/usr/bin/git log | head -n1 | cut -f2 -d' '"
gitsha = os.popen(git_cmd).read().strip('\n')
bug_project = project.lower()
bug_title = "Documentation bug"
html_context = {"gitsha": gitsha, "giturl": giturl,
                "bug_tag": "docs", "bug_title": bug_title,
                "bug_project": bug_project}

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'openstackdocs'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [openstackdocstheme.get_html_theme_path()]


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'monitorstackdoc'


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
    (master_doc, 'monitorstack.tex', u'monitorstack Documentation',
     u'OpenStack-Ansible Contributors', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'monitorstack', u'monitorstack Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'monitorstack', u'monitorstack Documentation',
     author, 'monitorstack', 'One line description of project.',
     'Miscellaneous'),
]


watermark = os.popen("git branch --contains $(git rev-parse HEAD)\
| awk -F/ '/stable/ {print $2}'").read().strip(' \n\t').capitalize()
if watermark == "":
    watermark = "Pre-release"

# -- Options for sphinxmark -----------------------------------------------
sphinxmark_enable = True
sphinxmark_div = 'docs-body'
sphinxmark_image = 'text'
sphinxmark_text = watermark
sphinxmark_text_color = (128, 128, 128)
sphinxmark_text_size = 70
