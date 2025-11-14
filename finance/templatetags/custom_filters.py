from django import template

register = template.Library()

@register.filter
def money(value):
    """Format number as UGX currency with comma separators"""
    try:
        value = float(value)
        return f"UGX {value:,.0f}"
    except (ValueError, TypeError):
        return value