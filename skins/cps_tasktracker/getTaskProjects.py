##parameters=key=None
#
# $Id$
"""A method to be used for a MethodVocabulary.

By contract to the MethodVocabulary class this method should handle a "key"
argument. If the key is not None then the method must return a value. And if
nothing was found, a KeyError should be raised.
"""

from logging import getLogger
logger = getLogger('CPSTaskTracker.getTaskProjects')

marker = []
value = marker
items = []

task_repository = getattr(context, 'tasks')
for project_item in task_repository.getProjects():
    project_id = project_item[0]
    project_title = project_item[1]['title']
    if key is None:
        items.append((project_id, project_title))
    elif project_id == key:
        value = project_id
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
