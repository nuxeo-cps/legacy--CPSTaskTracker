##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

title_from_fields = kw.get('title_from_fields', None)
if title_from_fields is not None:
    l = [kw.get(field, '').strip() for field in title_from_fields]
    l = filter(None, l)
    title = ' '.join(l)
    kw['title'] = title
    del kw['title_from_fields']

compute_dateiso = kw.get('compute_dateiso', None)
date = kw.get('date', None)
if compute_dateiso is not None and date is not None:
    dateiso = context.europeanDatify(date)
    #dateiso = DateTime().ISO() # XXX tmp
    kw['dateiso'] = dateiso
    del kw['compute_dateiso']

here = context.this()
here.edit(**kw)

if REQUEST is not None:
    psm = 'portal_status_message='+context.portal_messages('_cpsdocuments_Document_modified_')
    REQUEST.RESPONSE.redirect('%s/view?%s' % (here.absolute_url(), psm))
