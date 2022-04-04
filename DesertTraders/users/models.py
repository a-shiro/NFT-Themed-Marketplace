from django.contrib.auth import base_user
from django.contrib.auth import models as auth_models
from django.db import models

from DesertTraders.users.managers import CustomUserManager


class CustomUser(base_user.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False
    )

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    objects = CustomUserManager()
