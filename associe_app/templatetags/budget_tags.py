from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.simple_tag
def get_allocation(dictionary, poste_id, cat_type, cat_id, entreprise_id):
    """Returns the value from dictionary using string key."""
    if not dictionary:
        return ""
    c_id = int(cat_id) if cat_id else 0
    key = f"{poste_id}_{cat_type}_{c_id}_{entreprise_id}"
    return dictionary.get(key)

@register.simple_tag
def get_cat_type(poste_type):
    return 'pay' if poste_type == 'recette' else 'dep'

@register.filter
def sub(value, arg):
    try:
        return value - arg
    except (ValueError, TypeError):
        return 0
@register.simple_tag
def get_dict_value(dictionary, key):
    if not dictionary:
        return None
    return dictionary.get(str(key))

@register.filter
def format_comptable(value):
    """Formats a number as Algerian accounting format: 1.234,56 DA (negative in parentheses)"""
    if value is None:
        return "0,00 DA"
    try:
        val = float(value)
    except (ValueError, TypeError):
        return "0,00 DA"
    
    abs_val = abs(val)
    # Format with US defaults: 1,234.56
    formatted = "{:,.2f}".format(abs_val)
    # Swap separators to get 1.234,56
    # Note: we use temporary placeholders to avoid double swapping
    formatted = formatted.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
    
    res = f"{formatted} DA"
    if val < 0:
        res = f"({res})"
    return res
