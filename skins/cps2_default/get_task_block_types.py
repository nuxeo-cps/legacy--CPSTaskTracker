##parameters=

block_types = {
    'file': {
        'title': '_fd_block_file_',
        'template': 'block_file_template',
        'slots': [
            {
                'id': 'file',
                'type': 'file',
                'args': {
                }
            },
        ]
    },
    'hr': {
        'title': '_fd_block_hr_',
        'template': 'block_hr_template',
        'slots': []
    },
    'spacer': {
        'title': '_fd_block_spacer_',
        'template': 'block_spacer_template',
        'slots': []
    },
}
block_types.update(context.additional_block_types())

return block_types
