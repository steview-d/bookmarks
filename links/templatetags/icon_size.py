from django import template
register = template.Library()


@register.filter
def icon_size(value):
    # custom filter to calculate icon size based
    # on the value of display_mode
    return 48-((value-1)*16)
