##parameters=
# $Id$
"""Return CPSTaskTracker related vocabularies
"""

task_priority_vocabulary = {
    'data': {
        'dict': {
            'high': "High",
            'normal': "Normal",
            'low': "Low",
            },
        'list': [
            'high',
            'normal',
            'low',
            ],
        },
    }

task_type_vocabulary = {
    'data': {
        'dict': {
            'internal': "Internal",
            'nuxeo': "Nuxeo",
            'other': "Other",
            },
        'list': [
            'internal',
            'nuxeo',
            'other',
            ],
        },
    }

task_tracker_vocs = {}
task_tracker_vocs['task_priority'] = task_priority_vocabulary
task_tracker_vocs['task_type'] = task_type_vocabulary
return task_tracker_vocs
