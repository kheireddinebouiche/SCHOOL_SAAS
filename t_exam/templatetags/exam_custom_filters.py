from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def exam_get_item(dictionary, key):
    """
    Get an item from a dictionary using a variable key
    Usage: {{ mydict|exam_get_item:key_variable }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def exam_get_list_item(lst, index):
    """
    Get an item from a list using an index
    Usage: {{ mylist|exam_get_list_item:index_variable }}
    """
    try:
        return lst[index] if 0 <= index < len(lst) else None
    except (TypeError, IndexError):
        return None

@register.filter
def format_number_for_input(value):
    """
    Format a number for use in HTML input fields (convert to string with dot as decimal separator)
    Usage: {{ value|format_number_for_input }}
    """
    if value is None:
        return ''
    try:
        # Convert to float to ensure consistent decimal format
        float_value = float(value)
        # Format to string with dot as decimal separator
        return f"{float_value:g}"  # Use 'g' format to avoid unnecessary trailing zeros
    except (ValueError, TypeError):
        return str(value) if value is not None else ''