##parameters=
here = context.this()

common_fields = context.get_boxes_common_fields(here=here)

mcat = context.portal_messages

all_projects =  [{'title':x['title'], 'id':x['title']} for x in context.portal_tasks.getProjects()]
all_projects.append({'title':'', 'id':''})

fields = common_fields + [
    {
    'id': 'skinner',
    'title': '_label_skinner',
    'type': 'select',
    'value': context.skinner,
    'options': [{'title':x['title'], 'id':x['title']} for x in context.getTaskBoxSkinners()],
    },
    {
    'id': 'sort_date_on',
    'title': '_label_sort_date_on',
    'type': 'select',
    'value': context.sort_date_on,
    'options': context.getSortDateOn(),
    },
    {
    'id': 'sort_order',
    'title': '_label_sort_order',
    'type': 'select',
    'value': context.sort_order,
    'options': context.getSortOrder(),
    },
    {
    'id': 'sort_on',
    'title': '_label_sort_on',
    'type': 'select',
    'value': context.sort_on,
    'options': context.getSortOn(),
    },
    {
    'id': 'display_my_tasks',
    'title': '_label_display_my_tasks',
    'type': 'checkbox',
    'value': context.display_my_tasks,
    },
    {
    'id': 'display_my_affected_tasks',
    'title': '_label_display_my_affected_tasks',
    'type': 'checkbox',
    'value': context.display_my_affected_tasks,
    },
    {
    'id': 'display_my_groups_affected_tasks',
    'title': '_label_display_my_groups_affected_tasks',
    'type': 'checkbox',
    'value': context.display_my_groups_affected_tasks,
    },
    {
    'id': 'display_my_accepted_tasks',
    'title': '_label_display_my_accepted_tasks',
    'type': 'checkbox',
    'value': context.display_my_accepted_tasks,
    },
    {
    'id': 'display_on_project',
    'title': '_label_only_this_project',
    'type': 'select',
    'value': context.display_on_project,
    'options': all_projects,
    },
    ]

return here.basebox_edit_form(fields=fields)
