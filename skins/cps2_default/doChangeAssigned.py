## Script (Python) "doChangeAssigned"
##parameters=

"""
Re-assigning the task and re-opening this one.
"""

form = context.REQUEST.form
members = form.get('members', '')
groups  = form.get('groups', '')

context.changeAssigned(members=members, groups=groups)

return context.REQUEST.RESPONSE.redirect(context.absolute_url())
