import os, sys
sys.path.insert(0, os.path.abspath('..'))

project   = 'Mutual Information'
copyright = '2025-2026, Pranava BA'
author    = 'Pranava BA'
release   = '0.1.0'
version   = '0.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
]

templates_path   = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
master_doc       = 'index'

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'logo_only':                    False,
    'navigation_depth':             4,
    'titles_only':                  False,
    'collapse_navigation':          False,
    'sticky_navigation':            True,
    'includehidden':                True,
    'prev_next_buttons_location':   'both',
    'style_external_links':         True,
    'style_nav_header_background':  '#0f1629',
}

html_static_path = ['_static']
html_css_files   = ['css/custom.css']
html_title       = 'Mutual Information — ITF Docs'
html_short_title = 'mutual-information'

# html_logo    = '_static/img/itf_icon.png'
# html_favicon = '_static/img/itf_icon.png'

html_context = {
    'display_github':  True,
    'github_user':     'information-theory-finance',
    'github_repo':     'mutual-information',
    'github_version':  'main',
    'conf_py_path':    '/docs/',
}

mathjax3_config = {
    'tex': {
        'inlineMath':  [['$', '$'], ['\\(', '\\)']],
        'displayMath': [['$$', '$$'], ['\\[', '\\]']],
    }
}

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

copybutton_prompt_text      = r'>>> |\.\.\.\ |\$ '
copybutton_prompt_is_regexp = True
suppress_warnings           = ['toc.secnum']
