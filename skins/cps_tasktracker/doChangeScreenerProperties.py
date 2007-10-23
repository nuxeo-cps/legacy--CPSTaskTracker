##parameters=
#$Id$

"""Change the parameters given by the user form the UI
"""

form = context.REQUEST.form
context.updateParameters(form)

return context.REQUEST.RESPONSE.redirect(context.absolute_url())

