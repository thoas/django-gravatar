from django.conf import settings
from django.utils.hashcompat import md5_constructor
from urllib import urlencode

def _get_default_image_url(relative_path):
    """ This function has to be on top for old python interpreter. """
    from django.contrib.sites.models import Site
    return 'http://%s%s' % (Site.objects.get_current().domain, relative_path)

def get_gravatar(email, size = None, rating = None, default = None):
    '''
    Method returns URL string for gravatar image.
    Not only for template tag, also can be used as simple function
    '''
    gravatar_id = md5_constructor(email.lower()).hexdigest()
    gravatar_url = GRAVATAR_URL_PREFIX + gravatar_id + GRAVATAR_IMAGE_EXT

    if default:
        default = _get_default_image_url(default)

    # Build a list of tuples with Gravatar parameters that we want to use.
    #
    # This makes sure that no empty parameter will get appended to our final
    # URL, which makes it a little bit shorter and cleaner.
    parameters = [p for p in (
        ('d', default or GRAVATAR_DEFAULT_IMAGE),
        ('s', size or GRAVATAR_SIZE),
        ('r', rating or GRAVATAR_RATING),
    ) if p[1]]

    if parameters:
        gravatar_url += '?' + urlencode(parameters, doseq = True)

    return gravatar_url

GRAVATAR_URL_PREFIX = getattr(settings, 'GRAVATAR_URL_PREFIX', 'http://www.gravatar.com/avatar/')
GRAVATAR_IMAGE_EXT = getattr(settings, 'GRAVATAR_IMAGE_EXT', '')
GRAVATAR_RATING = getattr(settings, 'GRAVATAR_RATING', '')
GRAVATAR_SIZE = getattr(settings, 'GRAVATAR_SIZE', '')
GRAVATAR_DEFAULT_IMAGE = _get_default_image_url(getattr(settings, "GRAVATAR_DEFAULT_IMAGE")) if hasattr(settings, "GRAVATAR_DEFAULT_IMAGE") else ''