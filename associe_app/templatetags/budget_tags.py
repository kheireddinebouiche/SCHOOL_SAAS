from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))

@register.simple_tag
def get_allocation(dictionary, poste_id, cat_id, entreprise_id):
    """Returns the value from dictionary using (poste_id, cat_id, entreprise_id) tuple."""
    if not dictionary:
        return 0
    # cat_id can be 0 or None for direct poste assignment (legacy)
    c_id = int(cat_id) if cat_id else None
    return dictionary.get((int(poste_id), c_id, int(entreprise_id)))

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
