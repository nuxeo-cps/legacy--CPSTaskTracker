## Script (Python) "doChangeScreenerProperties"
##parameters=
#$Id$

"""
Change the poperties given by the usern form the UI
"""

form = context.REQUEST.form
context.changeScreenerProperties(form)

return context.REQUEST.RESPONSE.redirect(context.absolute_url())

