import bleach

from urllib import parse

from django.core.mail import mail_admins, send_mass_mail
from django.core.validators import URLValidator

from api.models import Fund, Comment, Entry
from vounty_backend.settings import GS_BUCKET_NAME


def handle_image(data):
    try:
        URLValidator(data)
        url = parse.unquote(data)
        path = 'https://storage.googleapis.com/' + GS_BUCKET_NAME + '/'
        if url.startswith(path):
            try: end = url.index('?')
            except ValueError: end = -1
            return url[len(path):end]
        raise ValueError()
    except Exception:
        return data


def sanitize(text):
    return bleach.clean(text, tags=['h1', 'h2', 'h3', 'p', 'strong', 'em', 's', 'u', 'a', 'blockquote',
                                    'ul', 'ol', 'li', 'i', 'code', 'acronym', 'abbr', 'b', 'hr'])


def send_email(vounty, user, type, text):
    subject = 'Someone commented in a vounty you\'re subscribed to!' if type == 0 else \
        'Someone submitted an entry in a vounty you\'re subscribed to!' if type == 1 else \
        'Someone has contributed some money to a vounty you\'re subscribed to!'
    intro = user.username + ' wrote:\n\n' + text + '\n\n' if type < 2 else ''
    message = intro + 'Check it out: https://vounty.io/vounty?id=' + str(vounty.id)

    emails = []
    user_id = [user.id]
    for comment in Comment.objects.filter(vounty_id=vounty.id):
        if comment.user.id in user_id: continue
        emails.append((subject, message, None, [comment.user.email]))
        user_id.append(comment.user.id)
    for entry in Entry.objects.filter(vounty_id=vounty.id):
        if entry.user.id in user_id: continue
        emails.append((subject, message, None, [entry.user.email]))
        user_id.append(entry.user.id)
    for fund in Fund.objects.filter(vounty_id=vounty.id):
        if fund.user.id in user_id: continue
        emails.append((subject, message, None, [fund.user.email]))
        user_id.append(fund.user.id)
    send_mass_mail(emails, fail_silently=True)

    # While there are few users in the platform, keep tabs on everything.
    mail_admins('New Activity in Vounty', message, fail_silently=True)
