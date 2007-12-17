##parameters=proxy, object, data, value
# $Id$
"""Reset the "dependency" field of a task document when the project changes.

This script is to be called as a "write_process_expr" script.
"""
from zLOG import LOG, DEBUG

LOG_KEY = 'CPSTaskTracker.resetTaskDependency'

#LOG('LOG_KEY', DEBUG, "data = %s" % data)
#LOG('LOG_KEY', DEBUG, "value = %s" % value)
#LOG('LOG_KEY', DEBUG, "proxy = %s" % proxy)
#LOG('LOG_KEY', DEBUG, "object = %s" % object)

# In the case of CPS tasks there are no proxies because we access directly the
# CPS documents which are stored directly in the tasks tool. But testing the
# proxy variable like this is a good way to know when we are in the case of the
# creation of the document. In this case there is never a dependency to reset.
if proxy is None:
    return value

#project_id = object.get('task_project')
project_id = object['task_project']
## LOG('LOG_KEY', DEBUG, "project_id before %s, after = %s"
##     % (project_id, data['task_project']))
if data['task_project'] != project_id:
    LOG('LOG_KEY', DEBUG,
        "Reseting the dependency since it is not in the same project")
    data['dependency'] = ''

return value
