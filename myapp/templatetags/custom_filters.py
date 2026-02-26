from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''

@register.filter
def replace_underscore(value):
    """Replace underscores with spaces"""
    if isinstance(value, str):
        return value.replace('_', ' ')
    return value

