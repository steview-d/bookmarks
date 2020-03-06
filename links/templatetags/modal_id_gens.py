# generate uniqiue id's for use with the 'delete_modal' template

from django import template
register = template.Library()


@register.filter
def bookmark_id(value):
    # return a unique id for the bookmark delete modal
    # using the pk of the bookmark object
    return f"modal-bm-{value}"


@register.filter
def collection_id(value):
    # return a unique id for the collection delete modal
    # using the collection name
    no_space = str(value).replace(' ', '_')
    return f"modal-{no_space}"
