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

@register.filter
def lookup(dictionary, key):
    """
    Get an item from a dictionary using a variable key
    Usage: {{ mydict|lookup:key_variable }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def range(value):
    """
    Return a range of numbers from 0 to value-1
    Usage: {% for i in value|range %}
    """
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)

@register.filter
def div(value, arg):
    """
    Divide value by arg
    Usage: {{ value|div:arg }}
    """
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def get_sous_note_by_index(builtin_type, index):
    """
    Get a sous-note by index from a builtin type
    Usage: {{ builtin_type|get_sous_note_by_index:index }}
    """
    try:
        sous_notes = list(builtin_type.sous_notes.all())
        if 0 <= index < len(sous_notes):
            return sous_notes[index]
        return None
    except Exception:
        return None

@register.filter
def getattr(obj, attr_name):
    """
    Get an attribute from an object by name
    Usage: {{ obj|getattr:"attribute_name" }}
    """
    try:
        return getattr(obj, attr_name, None)
    except:
        return None