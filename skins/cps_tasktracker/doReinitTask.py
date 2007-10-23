##parameters=

"""Close the task
"""

# Close the task.
context.reinitTask()

return context.REQUEST.RESPONSE.redirect(context.absolute_url())
