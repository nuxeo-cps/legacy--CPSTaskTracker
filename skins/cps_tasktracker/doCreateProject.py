##parameters=REQUEST=None
#
# $Id$
"""Create a new project
"""

if REQUEST is not None and \
   REQUEST.form is not None:
    form = REQUEST.form
    title = form.get('title', '')
    description = form.get('description', None)
    if title != []:
        new_project = {}
        new_project['id'] = context.computeId(title)
        new_project['title'] = title
        new_project['description'] = description
        context.tasks.addProject(new_project)

return context.REQUEST.RESPONSE.redirect(context.absolute_url()
                                         + '/cps_task_tool_manage_projects_form')
