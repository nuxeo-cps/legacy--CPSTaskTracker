## Script (Python) "getTaskBreadCrumb"
##parameters=REQUEST=None
#$Id$

"""Builts the breadcrumbs.

Will be empty except when we're coming
from the task screener.
"""

from zLOG import LOG, INFO


default_bc = [{'url': context.absolute_url(),
               'title': context.title_or_id(),
               'longtitle': context.title_or_id()
               }]

if REQUEST is None:
    return []
else:
    if REQUEST.get('skip_bc') is None:
        bc = REQUEST.SESSION.get('screener_breadcrumb')
        if bc is not None:
            stupid = 0
            for item in bc:
                if item['url'] == context.absolute_url():
                    #
                    # Here the title could have change.
                    # When you we just create a task.
                    #
                    item['title'] = context.title_or_id()
                    item['longtitle'] = context.title_or_id()
                    stupid = 1
            if stupid == 0:
                del bc[0]
                bc.append({'url': context.absolute_url(),
                           'title': context.title_or_id(),
                           'longtitle': context.title_or_id()
                           })
            return bc
        else:
            return default_bc
    else:
        if REQUEST.SESSION.has_key('screener_breadcrumb'):
            del REQUEST.SESSION['screener_breadcrumb']
        return default_bc
