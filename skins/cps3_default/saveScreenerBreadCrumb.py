##parameters=REQUEST=None
#$Id$

"""Save the breadcrumb of the screener.
"""

if REQUEST is not None:
    bc = context.breadcrumbs()
    return bc
    for item in bc:
        # FIXME here
        pass
        #del item['object']
    REQUEST.SESSION['screener_breadcrumb'] = bc
