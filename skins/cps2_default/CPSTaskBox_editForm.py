##parameters=
here = context.this()

common_fields = context.get_boxes_common_fields(here=here)

fields = common_fields + [
    {
    'id': 'sort_date_on',
    'title': 'label_sort_date_on',
    'type': 'select',
    'value': context.sort_date_on,
    'options': context.getSortDateOn(),
    },
    {
    'id': 'sort_order',
    'title': 'label_sort_order',
    'type': 'select',
    'value': context.sort_order,
    'options': context.getSortOrder(),
    },
    {
    'id': 'sort_on',
    'title': 'label_sort_on',
    'type': 'select',
    'value': context.sort_on,
    'options': context.getSortOn(),
    },
    {
    'id': 'display_my_tasks',
    'title': 'label_display_my_tasks',
    'type': 'checkbox',
    'value': context.display_my_tasks,
    },
    {
    'id': 'display_my_affected_tasks',
    'title': 'label_display_my_affected_tasks',
    'type': 'checkbox',
    'value': context.display_my_affected_tasks,
    },
    {
    'id': 'display_my_groups_affected_tasks',
    'title': 'label_display_my_groups_affacted_tasks',
    'type': 'checkbox',
    'value': context.display_my_groups_affected_tasks,
    },
    {
    'id': 'display_my_accepted_tasks',
    'title': 'label_display_my_accepted_tasks',
    'type': 'checkbox',
    'value': context.display_my_accepted_tasks,
    },
    ]

return here.basebox_edit_form(fields=fields)
