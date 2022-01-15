from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class BuyOrder(models.Model):
    user = models.ForeignKey(get_user_model(), unique=True,on_delete=models.CASCADE)
    order_price = models.FloatField()
    amount = models.FloatField()
    deposit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class SellOrder(models.Model):
    user = models.ForeignKey(get_user_model(), unique=True,on_delete=models.CASCADE)
    order_price = models.FloatField()
    amount = models.FloatField()
    deposit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Closedorder(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    position = models.CharField()
    closed_price = models.FloatField()
    amount = models.FloatField()
    deposit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Wallet(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    average_price = models.FloatField()
    amount = models.FloatField()