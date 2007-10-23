##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

here = context.this()
here.edit(**kw)

if REQUEST is not None:
    psm = 'portal_status_message='+'_cpsdocuments_Document_modified_'
    REQUEST.RESPONSE.redirect('%s/view?%s' % (here.absolute_url(), psm))
