from django import template

import string


register = template.Library()


@register.filter
def icon_size(value):
    # custom filter to calculate icon size based
    # on the value of display_mode
    return 48-((value-1)*16)


@register.filter
def icon_font_size(value):
    # custom filter to calculate icon size based
    # on the value of display_mode
    return (48-((value-1)*16))*0.75


@register.filter
def icon_letter(value):
    return value[0].upper()


@register.filter
def icon_color(value):
    colors_list = ['#698396',
                   '#a9c8c0',
                   '#dbbc8e',
                   '#ae8a8c',
                   '#f7f6cf',
                   '#e6a57e']

    char_list = string.ascii_uppercase
    idx = char_list.index(value[0].upper()) + 1
    return colors_list[idx % 6]
