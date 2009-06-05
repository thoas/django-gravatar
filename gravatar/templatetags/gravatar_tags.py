from django import template
from django.conf import settings
from hashlib import md5
from urllib import urlencode
import os.path
import urllib
import urlparse
import threading

GRAVATAR_URL_PREFIX = getattr(settings, 'GRAVATAR_URL_PREFIX', 'http://www.gravatar.com/avatar/')
GRAVATAR_IMAGE_EXT = getattr(settings, 'GRAVATAR_IMAGE_EXT', '')
GRAVATAR_DEFAULT_IMAGE = getattr(settings, 'GRAVATAR_DEFAULT_IMAGE', '')
GRAVATAR_RATING = getattr(settings, 'GRAVATAR_RATING', '')
GRAVATAR_SIZE = getattr(settings, 'GRAVATAR_SIZE', '')
GRAVATAR_CACHE_DIR = getattr(settings, 'GRAVATAR_CACHE_DIR', 'img/gravatar/')
GRAVATAR_MEDIA_PREFIX = getattr(settings, 'GRAVATAR_MEDIA_PREFIX', '/media/img/gravatar/')

register = template.Library()

def download_gravatar(url, dest):
    try:
        urllib.urlretrieve(url, dest)
    except IOError:
        pass

@register.simple_tag
def get_gravatar_for_email(email, size = None, rating = None):
    """
    Generates a Gravatar URL for the given email address.

    Syntax::

        {% get_gravatar_for_email <email> [size] [rating] %}

    Example::

        {% get_gravatar_for_email foobar@example.com 48 r %}
    """
    gravatar_id = md5(email.lower()).hexdigest()
    gravatar_url = GRAVATAR_URL_PREFIX + gravatar_id + GRAVATAR_IMAGE_EXT

    # Build a list of tuples with Gravatar parameters that we want to use.
    #
    # This makes sure that no empty parameter will get appended to our final
    # URL, which makes it a little bit shorter and cleaner.
    parameters = [p for p in (
        ('d', GRAVATAR_DEFAULT_IMAGE),
        ('s', size or GRAVATAR_SIZE),
        ('r', rating or GRAVATAR_RATING),
    ) if p[1]]

    if parameters:
        gravatar_url += '?' + urlencode(parameters, doseq = True)

    gravatar_local = os.path.join(settings.MEDIA_ROOT, GRAVATAR_CACHE_DIR, '%s.jpg' % gravatar_id)

    if not os.path.isfile(gravatar_local):
        t = threading.Thread(
            target = download_gravatar,
            args = (
                gravatar_url, 
                gravatar_local
            )
        )

        t.setDaemon(True)
        t.start()

        return gravatar_url

    return urlparse.urljoin(GRAVATAR_MEDIA_PREFIX, '%s.jpg' % gravatar_id)
