##parameters=REQUEST=None
#$Id$

"""
Save the breadcrumb of the screener.
"""

if REQUEST is not None:
    bc = context.breadcrumbs()
    for item in bc:
        del item['object']
    REQUEST.SESSION['screener_breadcrumb'] = bc
