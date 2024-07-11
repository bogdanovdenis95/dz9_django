from django import template

register = template.Library()


@register.filter
def media_url(value):
    if value:
        return f'/media/{value}'
    return '#'
