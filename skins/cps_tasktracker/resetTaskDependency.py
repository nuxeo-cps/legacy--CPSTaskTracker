##parameters=proxy, object, data, value
# $Id$
"""Reset the "dependency" field of a task document when the project changes.

This script is to be called as a "write_process_expr" script.
"""
from zLOG import LOG, DEBUG


#LOG('XXXX', DEBUG, "data = %s" % data)
#LOG('XXXX', DEBUG, "value = %s" % value)
#LOG('XXXX', DEBUG, "proxy = %s" % proxy)
#LOG('XXXX', DEBUG, "object = %s" % object)

# In the case of CPS tasks there are no proxies because we access directly the
# CPS documents which are stored directly in the tasks tool. But testing the
# proxy variable like this is a good way to know when we are in the case of the
# creation of the document. In this case there is never a dependency to reset.
if proxy is None:
    return value

#project_id = object.get('task_project')
project_id = object['task_project']
#LOG('XXXX', DEBUG, "project_id before %s, after = %s" % (project_id, data['task_project']))
if data['task_project'] != project_id:
    data['dependency'] = ''

return value
