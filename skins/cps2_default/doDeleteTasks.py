## Script (Python) "doDeleteTasks.py"
##parameters=ids=[]
#$Id$

"""
Delete all the tasks choosen from the Screen UI.
"""

REQUEST = context.REQUEST

from zLOG import LOG, DEBUG
LOG("DELETE CANDIDATE TASKS", DEBUG, ids)

ptasks = context.portal_tasks
#
# Flag to check if the delete operation is allowed.
# Just for security cause we are not going to let
# the user the possiblity to do it.
# But he can still try by calling the method...
#
not_allowed = 0
psm = 'task_deleted'

for id in ids:
    try:
        ptasks.manage_delObjects([id])
    except:
        not_allowed = 1

# Do something if the member is not allowed to do it with the help of the flag.
return REQUEST.RESPONSE.redirect('.')
