##parameters=REQUEST=None, **kw
#$Id$
"""Create a Task
"""

from urllib import urlencode

#
# The task are created in the portal_tasks
# It might be possible to create them elsewhere such as workspaces
# somewhere else with slight modifications.
#

task_repository = context.portal_tasks

type_name = 'CPS Task'
id = context.computeId()
task_repository.invokeFactory(type_name, id)

new_task = getattr(task_repository, id)
return REQUEST.RESPONSE.redirect('%s/%s/cpsdocument_edit_form' %
                                 (task_repository.absolute_url(),
                                  id))
