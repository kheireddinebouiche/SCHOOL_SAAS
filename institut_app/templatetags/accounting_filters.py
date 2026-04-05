from django import template

register = template.Library()


@register.filter(name='format_dzd')
def format_dzd(value, decimals=0):
    """
    Format a number as Algerian accounting format.
    Example: 1234567.89 -> '1 234 567,89 DA'
    Usage in template: {{ value|format_dzd }} or {{ value|format_dzd:2 }}
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value

    decimals = int(decimals)

    # Format with the appropriate decimal places
    if decimals == 0:
        formatted = f"{value:,.0f}"
    else:
        formatted = f"{value:,.{decimals}f}"

    # Replace commas (thousands) with spaces and periods (decimal) with commas
    # First replace decimal point with a placeholder
    formatted = formatted.replace('.', '§')
    # Then replace thousands comma separator with space
    formatted = formatted.replace(',', ' ')
    # Finally restore decimal separator as comma
    formatted = formatted.replace('§', ',')

    return f"{formatted} DA"
