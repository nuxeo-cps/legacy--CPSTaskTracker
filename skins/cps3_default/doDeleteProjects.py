##parameters=ids=[]
#$Id$

"""Delete all the projects choosen from the Screen UI.
"""

REQUEST = context.REQUEST

from zLOG import LOG, DEBUG
LOG("DELETE CANDIDATE PROJECTS", DEBUG, ids)

ptasks = context.portal_tasks
psm = 'projects_deleted'

if same_type(ids, ''):
    ids = [ids]

for id in ids:
        ptasks.delProjects(ids)

return context.REQUEST.RESPONSE.redirect(context.absolute_url()+'/cps_task_tool_manage_projects_form')
