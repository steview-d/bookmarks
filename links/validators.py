from django.core.exceptions import ValidationError

import os


def validate_icon_file_extension(value):
    """
    Validator to ensure only specific filetypes can be used for
    bookmark icons
    """
    f_ext = os.path.splitext(value.name)[1]
    allowed_types = ['.png', '.jpg', '.jpeg']

    if f_ext not in allowed_types:
        raise ValidationError(
            u'Your file must be either .png or .jpg \
                - please choose a different file.')


def validate_icon_file_size(value):
    """
    Validator to ensure uploaded icon is below a certain size
    Currently set to 3145728 bytes / 3MB
    """
    f_size = value.size

    if f_size > 3145728:
        raise ValidationError(
            u'Your file exceeds the maximum allowed size of 3MB - \
                please choose a different file.')
