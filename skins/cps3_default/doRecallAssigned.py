## Script (Python) "doRecallAssigned"
##parameters=REQUEST=None

"""Recalling the assigned.

Sending a mail to the choosen ones.
"""

mcat = context.Localizer.default
def mcatIso(s):
    """Encode iso
    """
    return mcat(s).encode("ISO-8859-15", 'ignore')

if REQUEST is not None and \
   REQUEST.form.has_key('ids'):
    #
    # Getting the emails from the request
    #
    ids = REQUEST.form.get('ids', [])
    if same_type(ids, ''):
        ids = [ids]
    emails = ids
    #
    # Then formating them for the 'to' field
    #
    mails = ""
    for email in emails:
        mails += email + ';'

    # Here the list of mails ready to be sent.
    emails = mails[:-1]
    # Then the mail from the member who's recalling the tribe.
    from_address = context.portal_membership.getAuthenticatedMember().getProperty('email')


    content = "\n\n" \
              + mcatIso('_label_you_are_recalled_for_the_task') \
              + " " \
              + "<a href=" \
              + context.absolute_url() \
              + ">" \
              + context.title_or_id() \
              + "</a>" \
              + "\n\n"

    subject = mcatIso('_label_recall') \
              + " : " \
              + context.title_or_id()


    header = "From: %s\n" % from_address \
             + "Reply-to: %s\n" % from_address \
             + "To: %s\n" % emails \
             + "Subject: %s\n" % subject \
             + 'Content-Type: multipart/alternative; boundary="=-vW5qqYDB5ezCu1fyKpxA"\n' \
             + 'Mime-Version: 1.0\n'

    body = header + '\n\n' \
           + '--=-vW5qqYDB5ezCu1fyKpxA\n' \
           + 'Content-Type: text/plain; charset=iso-8859-1\n' \
           + 'Content-Transfer-Encoding: 8bit\n\n' \
           + content \
           + '\n\n' \
           + '--=-vW5qqYDB5ezCu1fyKpxA\n' \
           + 'Content-Type: text/html; charset=iso-8859-1\n\n' \
           + content \
           + '\n\n' \
           + '--=-vW5qqYDB5ezCu1fyKpxA--\n'


    #
    # Then sending the mail
    #
    stupid = context.sendMailTo(content=body,
                                emails=ids,
                                from_address=from_address,
                                subject=subject,
                                )

    if stupid:
        stupid_psm = mcatIso('_label_mail_sent')
    else:
        stupid_psm = mcatIso('_label_error_while_sending_mail')

psm = '/?portal_status_message=%s' %(stupid_psm)
return context.REQUEST.RESPONSE.redirect(context.absolute_url() + psm)
