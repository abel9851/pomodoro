from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """custom user model"""

    class Meta:
        db_table = "users"

    # TODO: profile 추가 ImageField
    email = models.EmailField(_("email address"), unique=True)

    def __str__(self):
        return self.username
