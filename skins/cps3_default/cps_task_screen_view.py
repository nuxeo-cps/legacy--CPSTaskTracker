## Script (Pyhton) "cps_task_screen_view.py"
##parameters=

#$Id$

"""
Return the skinner for the task screen.
Rendering it according to the screener.
"""

render_template = "cps_task_screen_view_template"
all_skinners = context.getTaskScreenSkinners()

for skin in all_skinners:
    if skin.get('title') == context.skinner:
        render_template = skin.get('zpt')

return context.REQUEST.RESPONSE.redirect(context.absolute_url()+"/"+render_template)




