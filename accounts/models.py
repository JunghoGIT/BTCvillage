from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    usdt = models.FloatField(default=100000)

    def __str__(self):
        return self.username


