##parameters=block_type, before_block=None, REQUEST=None

block_id = context.addFlexibleBlock(block_type, before_block)

if REQUEST is not None:
    url = '%s/cps_task_edit_form' % (context.absolute_url(), )
    if block_id:
        url = '%s#%s' % (url, block_id)
    REQUEST.RESPONSE.redirect(url)
