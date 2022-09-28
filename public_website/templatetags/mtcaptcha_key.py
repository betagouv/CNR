from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_mtcaptcha_public_key():
    return settings.MTCAPTCHA_PUBLIC_KEY
