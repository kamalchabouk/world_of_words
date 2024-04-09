from django import template

register = template.Library()

@register.filter(name='remove_prefix')
def remove_prefix(value):
    return value.replace('media/images/', '')
