##parameters=ids=[], project_id=None
#$Id$

"""Delete all the tasks choosen from the Screen UI.
"""

REQUEST = context.REQUEST

from zLOG import LOG, DEBUG
LOG("DELETE CANDIDATE TASKS", DEBUG, ids)

ptasks = context.tasks

# Flag to check if the delete operation is allowed.
# Just for security cause we are not going to let
# the user the possiblity to do it.
# But he can still try by calling the method...
#
not_allowed = False
psm = 'task_deleted'

for id in ids:
    # XXX : fixing rights on the repository itself.
    try:
        ptasks.manage_delObjects([id])
    except:
        not_allowed = True

# TODO: Do something if the member is not allowed to do it (thanks to the flag)

utool = context.portal_url
portal = utool.getPortalObject()
portal_absolute_url = portal.absolute_url()
return REQUEST.RESPONSE.redirect('%s/cps_task_project_edit_form?project_id=%s'
                                 % (portal_absolute_url, project_id))
