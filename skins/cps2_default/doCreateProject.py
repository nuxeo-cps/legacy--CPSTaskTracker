## Script (Python) "doCreateProject"
##parameters=REQUEST=None

"""
Create a new project
"""

from zLOG import LOG, DEBUG

#
# XXX : not finished
#

if REQUEST is not None and \
   REQUEST.form is not None:
    form = REQUEST.form
    title = form.get("title", "")
    description = form.get("description", "")
    if title != []:
        new_project = {}
        new_project['title'] = title
        new_project['description'] = description
        context.portal_tasks.addProject(new_project)

return context.REQUEST.RESPONSE.redirect(context.absolute_url()+'/cps_task_tool_manage_projects_form')
