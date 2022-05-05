from django.core.exceptions import ValidationError


def max_image_size(image_file):
    filesize = image_file.file.size
    megabyte_limit = 5.0

    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError('Max file size is 5.00 MB')