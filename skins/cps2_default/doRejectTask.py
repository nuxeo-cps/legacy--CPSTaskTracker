## Script (Python) "doRejectTask"
##parameters=

"""
The member is rejecting the task.
"""

# Reject the task.
context.rejectTask()

return context.REQUEST.RESPONSE.redirect(context.absolute_url())
