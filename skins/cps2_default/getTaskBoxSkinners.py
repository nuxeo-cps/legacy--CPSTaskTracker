## Script (Pyhton) "getTaskScreenSkinners"
##parameters=

#$Id$

"""
Default skinners.
It calls the getCustomTaskBoxSkinners script if you
wanna use your templates.
Check the example in the getCustomTaskBoxSkinners
"""

box_skinners = []

nuxeo_skin = {'title':'default',
              'zpt':'CPSTaskBox_renderBodyTemplate'}

box_skinners.append(nuxeo_skin)

#
# Here calling the custom skinners script in case of.
#
for cskinner in context.getCustomTaskBoxSkinners():
    box_skinners.append(cskinner)

return box_skinners

