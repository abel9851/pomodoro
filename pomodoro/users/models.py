from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """custom user model"""

    # profile_image =
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
