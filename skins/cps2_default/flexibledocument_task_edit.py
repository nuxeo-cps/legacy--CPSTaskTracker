##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

redirect_block = context.edit(**kw)

if REQUEST is not None:
    url = '%s/cps_task_edit_form' % (context.absolute_url(), )
    if redirect_block:
        url = '%s#%s' % (url, redirect_block)
    REQUEST.RESPONSE.redirect(url)
