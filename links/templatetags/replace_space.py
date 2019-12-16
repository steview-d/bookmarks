from django import template
register = template.Library()


@register.filter
def replace_space(value):
    # custom filter to replace a space char with an underscore
    # intended use is for generating HTML ID's from collection names
    return str(value).replace(' ', '_')
