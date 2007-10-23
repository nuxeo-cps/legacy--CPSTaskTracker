## Script (Python) "get_date.py"
##parameters=cdate=None, id=None, fmt=None
#$Id$

"""Return the date according to the current language
"""

from zLOG import LOG, DEBUG

from DateTime import DateTime
from re import match

fmt = "%m/%d/%Y"
lang = context.Localizer.default.get_selected_language()

if cdate:
    if lang == 'fr':
        d, m, y = cdate.split('/')
        fmt = "%d/%m/%Y"
    else:
        m, d, y = cdate.split('/')
        fmt = "%m/%d/%Y"

    try:
        dtv = DateTime(int(y), int(m), int(d), 0, 0)
    except:
        y, m, d = cdate.split('/')
        dtv = DateTime(int(y), int(m), int(d), 0, 0)
else:
    dtv = DateTime()
    if lang == 'fr':
        fmt = "%d/%m/%Y"

return {'day':dtv.day(),
        'month':dtv.month(),
        'year':dtv.year(),
        'all':dtv.strftime(fmt),
        'for_storing': dtv.strftime("%m/%d/%Y")}
