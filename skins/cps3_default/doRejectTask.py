##parameters=

"""The member is rejecting the task.
"""

# Reject the task.
context.rejectTask()

mcat = context.Localizer.default
def mcatIso(s):
    """Encode iso
    """
    try:
        return mcat(s).encode("ISO-8859-15", 'ignore')
    except (UnicodeDecodeError,):
        return mcat(s)

creator_email = context.portal_directories.members.getEntry(context.Creator(), {}).get('email', None)
current_member = context.portal_directories.members.getEntry(context.portal_membership.getAuthenticatedMember().getMemberId(), {})

content = "\n\n" \
          + mcatIso('_label_the_task_has_been_rejected') \
          + " " \
          + "<a href=" \
          + context.absolute_url() \
          + ">" \
          + context.title_or_id() \
          + "</a>" \
          + mcatIso('_label_by') \
          + " <a href=" \
          + context.absolute_url() + "/cpsdirectory_entry_view?dirname=members&id=" \
          + current_member.get('id') \
          + ">" \
          + current_member.get('fullname') \
          + "</a>" \
          + "\n\n"


subject = mcatIso('_label_task_rejected') \
          + " : " \
          + context.title_or_id()


header = "From: %s\n" % creator_email \
         + "Reply-to: %s\n" % creator_email \
         + "To: %s\n" % creator_email \
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

stupid = 0
if creator_email is not None:
    stupid = context.sendMailTo(content=body,
                                emails=creator_email,
                                from_address=creator_email,
                                subject=subject,
                                )

if stupid:
    stupid_psm = mcatIso('_label_mail_sent')
else:
    stupid_psm = mcatIso('_label_error_while_sending_mail')

psm = '/?portal_status_message=%s' %(stupid_psm)
return context.REQUEST.RESPONSE.redirect(context.absolute_url() + psm)
