##parameters=

portal = context.portal_url.getPortalObject()
task_repository = portal.portal_tasks

return task_repository.cps_task_edit_form(create=1)
