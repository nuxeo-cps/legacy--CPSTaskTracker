##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

kw['create']=1
kw['type_name']=kw['base']

portal = context.portal_url.getPortalObject()
task_repository = portal.portal_tasks

context = task_repository

ob, psm = context.cpsdocument_create(**kw)

base_id = kw.get('base')

if base_id is not None:
    bases = context.get_flexibledocument_bases()
    for base in bases:
        if base['id'] == base_id:
            blocks = base['blocks']
            for block_type in blocks:
                ob.addFlexibleBlock(block_type)
            lock_layout = base.get('lock_layout')
            if lock_layout:
                ob.lockDocumentLayout()

if REQUEST is not None:
    REQUEST.RESPONSE.redirect('%s/cps_task_edit_form?%s' % (ob.absolute_url(), psm))
else:
    return id
