##parameters=ids=[]
#$Id$

"""Delete all the projects choosen from the Screen UI.
"""

REQUEST = context.REQUEST

ptasks = context.tasks
psm = 'projects_deleted'

if same_type(ids, ''):
    ids = [ids]

ptasks.delProjects(ids)

return context.REQUEST.RESPONSE.redirect(context.absolute_url()+'/cps_task_tool_manage_projects_form')
