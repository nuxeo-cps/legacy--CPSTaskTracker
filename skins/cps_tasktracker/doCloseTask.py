##parameters=

"""Member who accepted the task
is closing it.
"""

# Accept the task.
context.closeTask()

return context.REQUEST.RESPONSE.redirect(context.absolute_url())
