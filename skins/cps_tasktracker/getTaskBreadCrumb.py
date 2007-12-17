##parameters=REQUEST=None
# $Id$
"""Builts the breadcrumbs.

Sets the breadcrumb as if a task had its project as parent.
"""

from zLOG import LOG, DEBUG, INFO

from Products.CMFCore.utils import getToolByName

utool = getToolByName(context, 'portal_url')
tasktool = getToolByName(context, 'tasks')

portal = utool.getPortalObject()
portal_url = portal.absolute_url()

bc = [{'url': portal_url,
       'title': portal.title_or_id(),
       'longtitle': portal.title_or_id(),
       }]

project_id = context['task_project']
if not project_id:
    return bc

project_def = tasktool.getProjectDef(project_id)
project_title = project_def['title']
project_url = portal_url + '/cps_task_project_view?project_id=' + project_id

bc.append({'url': project_url,
            'title': project_title,
            'longtitle': project_title,
           })

bc.append({'url': context.absolute_url(),
            'title': context.title_or_id(),
            'longtitle': context.title_or_id(),
           })

return bc

