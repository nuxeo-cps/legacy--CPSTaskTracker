##parameters=REQUEST=None
#$Id$

"""Save the breadcrumb of the screener.
"""

from zLOG import LOG, INFO

if REQUEST is not None:
    bc = context.breadcrumbs()
    REQUEST.SESSION['screener_breadcrumb'] = bc
