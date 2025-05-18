from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(key, str):
        key = key.strip()
    return dictionary.get(key)

