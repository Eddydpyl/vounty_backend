import bleach

from urllib import parse

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
