## Script (Python) "get_date.py"
##parameters=cdate=None, id=None, fmt=None
#$Id$

"""
Return the date according to the current language
"""

from zLOG import LOG, DEBUG

from DateTime import DateTime
from re import match

fmt = "%m/%d/%Y"
lang = context.portal_messages.get_selected_language()

if cdate and match(r'^[0-9]{4,4}/[0-9]?[0-9]/[0-9]?[0-9]$', cdate):
    if lang == 'fr':
        y, m, d = cdate.split('/')
        fmt = "%d/%m/%Y"
    else:
        y, m, d = cdate.split('/')
        fmt = "%m/%d/%Y"
    try:
        dtv = DateTime(int(y), int(m), int(d), 0, 0)
    except:
        dtv = DateTime()
else:
    dtv = DateTime()
    if lang == 'fr':
        fmt = "%d/%m/%Y"

return {'day':dtv.day(),
        'month':dtv.month(),
        'year':dtv.year(),
        'all':dtv.strftime(fmt)}
