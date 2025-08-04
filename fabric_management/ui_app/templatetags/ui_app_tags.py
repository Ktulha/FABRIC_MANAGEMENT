from django import template
register = template.Library()


@register.filter('multiply')
def multiply(value, arg):
    if not arg:
        arg = 1
    return value*arg
