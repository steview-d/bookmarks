from django import template

from random import randint


register = template.Library()


@register.simple_tag
def random_int(num):
    """
    Return a random number between 1 and 'num'
    """
    return randint(1, num)
