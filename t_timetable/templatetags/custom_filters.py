from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using a variable key
    Usage: {{ mydict|get_item:key_variable }}
    """
    try:
        return dictionary.get(key)
    except AttributeError:
        return None