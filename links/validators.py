from django.core.exceptions import ValidationError

import os


def validate_icon_file_extension(value):
    """
    Validator to ensure only specific filetypes can be used for
    bookmark icons
    """
    f_ext = os.path.splitext(value.name)[1].lower()
    allowed_types = ['.png', '.jpg', '.jpeg', '.ico']

    if f_ext not in allowed_types:
        raise ValidationError(
            u'Your file must be either .png, .jpg, or .ico \
                - please choose a different file.')


def validate_icon_file_size(value):
    """
    Validator to ensure uploaded icon is below a certain size
    Currently set to 2097152 bytes / 2MB
    """
    f_size = value.size

    if f_size > 2097152:
        raise ValidationError(
            u'Your file exceeds the maximum allowed size of 2MB - \
                please choose a different file.')
