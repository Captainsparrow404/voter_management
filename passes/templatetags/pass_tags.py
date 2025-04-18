from django import template

register = template.Library()

@register.filter
def status_class(value):
    return f'status-{value.lower()}'