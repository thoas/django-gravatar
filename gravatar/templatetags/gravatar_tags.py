from django import template
from gravatar import get_gravatar

register = template.Library()

@register.simple_tag
def get_gravatar_for_email(email, size = None, rating = None):
    """
    Generates a Gravatar URL for the given email address.

    Syntax::

        {% get_gravatar_for_email <email> [size] [rating] %}

    Example::

        {% get_gravatar_for_email foobar@example.com 48 r %}
    """
    return get_gravatar(email, size, rating)