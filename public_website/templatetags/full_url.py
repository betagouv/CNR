from django import template

register = template.Library()

@register.simple_tag
def full_url(request):
    return request.build_absolute_uri().rstrip('/')