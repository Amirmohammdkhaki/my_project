from django import template

register = template.Library()

@register.filter
def dict_key(d, key):
    """فیلتر برای دسترسی به مقدار dictionary با key"""
    return d.get(key, 0)

@register.filter
def sum(values):
    """فیلتر برای جمع مقادیر"""
    return sum(values)