## Script (Pyhton) "getTaskScreenSkinners"
##parameters=

#$Id$

"""
Default skinners.
It calls the getCustomTaskScreenSkinners script if you
wanna use your templates.
Just follow the same struct as below.
"""

screen_skinners = []

nuxeo_skin = {'title':'nuxeo',
              'zpt':'cps_task_screen_view_template'}

screen_skinners.append(nuxeo_skin)

#
# Here calling the custom skinners script in case of.
#
for cskinner in context.getCustomTaskScreenSkinners():
    screen_skinners.append(cskinner)

return screen_skinners

