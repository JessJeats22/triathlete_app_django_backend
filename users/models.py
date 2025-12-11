from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True)
    profile_image = models.URLField(blank=True, null=True)
    favourited_trails = models.ManyToManyField(
        to='trails.Trail',
        related_name='favourited_by_users'
    )