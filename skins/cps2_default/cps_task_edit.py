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


if kw.get('parameters'):
    # Dates localized
    start_date = kw.get('start_task_date', None)
    if start_date is not None:
        kw['start_task_date'] = context.get_date(start_date)['for_storing']

    stop_date = kw.get('stop_task_date', None)
    if stop_date is not None:
        kw['stop_task_date'] = context.get_date(stop_date)['for_storing']

here = context.this()
here.edit(**kw)

if REQUEST is not None:
    psm = 'portal_status_message='+context.portal_messages('_cpsdocuments_Document_modified_')
    REQUEST.RESPONSE.redirect('%s?%s' % (here.absolute_url()+"/cps_task_edit_parameters_form", psm))
