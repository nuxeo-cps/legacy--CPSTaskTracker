##parameters=
# $Id$
"""Return CPSTaskTracker related vocabularies
"""

task_priority_vocabulary = {
    'data': {
        'dict': {
            'high': "label_priority_high",
            'normal': "label_priority_normal",
            'low': "label_priority_low",
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
            'internal': "label_priority_internal",
            'nuxeo': "label_priority_nuxeo",
            'other': "label_priority_other",
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
