from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Openorder(models.Model):
    user = models.ForeignKey(get_user_model(), unique=True,on_delete=models.CASCADE)
    open_price = models.FloatField()
    limited_price = models.FloatField()
    margin = models.IntegerField()
    amount = models.FloatField()
    deposit = models.FloatField()
    liquidation_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    buy = models.BooleanField()
    sell = models.BooleanField()


class Closedorder(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    opened_price = models.FloatField()
    closed_price = models.FloatField()
    margin = models.IntegerField()
    amount = models.FloatField()
    deposit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)