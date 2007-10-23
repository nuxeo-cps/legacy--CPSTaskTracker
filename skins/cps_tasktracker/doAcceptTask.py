##parameters=

"""Set the member assigned to this task
cause he choose it.
"""

# Accept the task.
context.acceptTask()

return context.REQUEST.RESPONSE.redirect(context.absolute_url())
