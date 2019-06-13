from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class UserProfile(AbstractUser):
    """User details
    """
    create_time = models.DateField(default=datetime.now)
    create_by = models.CharField(default='', max_length=250)  # create by whom

