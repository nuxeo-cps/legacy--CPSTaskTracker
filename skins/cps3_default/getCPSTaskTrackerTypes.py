## Script (Python) "getCPSTaskTrackerTypes"
##parameters=
# $Id$
"""CPSTaskTracker content type definition
"""

cps_task_type = {
    'title': 'portal_type_CPS_Task_title',
    'description': 'portam_type_CPS_Task_description',
    'content_icon': 'task_icon.png',
    'content_meta_type': 'CPS Task',
    'product': 'CPSTaskTracker',
    'factory': 'addCPSTask',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': '',
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    'cps_proxy_type': 'document',
    'cps_display_as_document_in_listing': 0,
    'schemas': ['metadata', 'common', 'cps_task', 'flexible_content'],
    'layouts': ['cps_task', 'flexible_content'],
    'flexible_layouts': ['flexible_content:flexible_content'],
    'storage_methods': [],
}

task_tracker_types = {}
task_tracker_types['CPS Task'] = cps_task_type
return task_tracker_types
