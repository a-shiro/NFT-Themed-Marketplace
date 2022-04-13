from django.contrib.auth import models as auth_models
from django.db import models
from django.core import validators as django_validators
from django.contrib.auth import base_user

from DesertTraders.users.managers import CustomUserManager


class CustomUser(base_user.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'email'

    ERROR_MESSAGE_FOR_UNIQUE = 'This email has already been registered.'

    REGEX_PATTERN_FOR_EMAIL_VALIDATOR = "^([a-z\d\.-]+)@([a-z\d-]+)\.([a-z]{2,8})(\.[a-z]{2,8})?$"
    REGEX_ERROR_MESSAGE = 'Please enter a valid email address.'

    email = models.EmailField(
        unique=True,
        validators=(
            django_validators.RegexValidator(
                REGEX_PATTERN_FOR_EMAIL_VALIDATOR,
                REGEX_ERROR_MESSAGE
            ),
        ),
        error_messages={
            'unique': ERROR_MESSAGE_FOR_UNIQUE,
        },
    )

    is_staff = models.BooleanField(
        default=False
    )

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    objects = CustomUserManager()
