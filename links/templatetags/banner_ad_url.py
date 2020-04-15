from django import template

from random import randint


register = template.Library()


@register.filter
def create_ad_url(path, ext):
    """
    create a url to the ad image file

    adjust the second arg of randint to match the total
    mumber of ads in rotation, ensuring ads files are named
    ad1, ad2, upto ad(x)
    """

    # generate a random number that matches to one of the available banner ads
    ad_num = randint(1, 5)
    return str(path) + str(ad_num) + str(ext)
