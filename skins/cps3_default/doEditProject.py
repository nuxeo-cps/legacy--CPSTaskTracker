##parameters=REQUEST=None
#
# $Id$
"""Create a new project
"""

from urllib import urlencode

from logging import getLogger
logger = getLogger('doEditProject')


logger.debug("1")
form = REQUEST.form
logger.debug("2")
project_id = form.get('project_id')
logger.debug("3")
title = form.get('title')
logger.debug("4")
description = form.get('description')
logger.debug("5")
project_def = {}
logger.debug("6")
project_def['id'] = project_id
logger.debug("7")
project_def['title'] = title
logger.debug("8")
project_def['description'] = description
logger.debug("9")
context.tasks.editProject(project_def)
logger.debug("10")

args = {'project_id': project_id}
logger.debug("11")
return context.REQUEST.RESPONSE.redirect('%s/cps_task_project_edit_form?%s'
                                         % (context.absolute_url(),
                                            urlencode(args)))
