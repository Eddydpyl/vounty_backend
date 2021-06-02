import bleach

from urllib import parse

from django.core.mail import mail_admins, send_mass_mail
from django.core.validators import URLValidator

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


def send_email(vounty, user, subscriptions, subject, text):
    intro = user.username + ' wrote:\n\n' + text + '\n\n' if text is not None else ''
    message = intro + 'Check it out: https://vounty.io/vounty?id=' + str(vounty.id)

    emails = []
    for subscription in subscriptions:
        emails.append((subject, message, None, [subscription.user.email]))
    send_mass_mail(emails, fail_silently=True)

    # While there are few users in the platform, keep tabs on everything.
    mail_admins('New Activity in Vounty', message, fail_silently=True)
