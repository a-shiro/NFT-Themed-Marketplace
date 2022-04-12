from django.core import exceptions as django_exceptions


def alphanumeric_validator(username):
    if not username.isalnum():
        raise django_exceptions.ValidationError('Username must contain only letters and numbers.')

