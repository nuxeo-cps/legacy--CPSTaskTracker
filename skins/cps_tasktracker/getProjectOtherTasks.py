##parameters=key=None
#
# $Id$
"""A method to be used for a MethodVocabulary.

By contract to the MethodVocabulary class this method should handle a "key"
argument. If the key is not None then the method must return a value. And if
nothing was found, a KeyError should be raised.
"""

from logging import getLogger
logger = getLogger('CPSTaskTracker.getProjectTasks')
#logger.debug("context = %s\n\n" % context)

marker = []
value = marker
items = []

# The context here is the doc and not the proxy because the task repository
# contains docs and not proxies. Using proxies in this context is useless.
# So the following code is useless:
#doc = context.getContent()

project_id = getattr(context, 'task_project', None)
#logger.debug("project_id = %s\n\n" % project_id)

task_repository = getattr(context, 'tasks')
task_defs = []
if project_id is not None:
    task_defs = task_repository.getProjectTasks(project_id)
    #logger.debug("task_defs = %s\n\n" % task_defs)

for task_def in task_defs:
    task_id = task_def['id']
    task_title = task_def['title']
    if key is None and task_id != context.getId():
        items.append((task_id, task_title))
    elif task_id == key:
        value = task_id
        break

if key is not None:
    if value is not marker:
        return value
    else:
        # This case will be catched by the MethodVocabulary which will return a
        # default value.
        raise KeyError
else:
    return items

