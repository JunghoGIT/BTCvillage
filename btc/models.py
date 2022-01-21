from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    order_price = models.FloatField(unique=True)
    amount = models.FloatField()
    deposit = models.FloatField()
    position = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


class ClosedOrder(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    closed_price = models.FloatField()
    amount = models.FloatField()
    deposit = models.FloatField()
    position = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)


class Wallet(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,unique=True)
    average_price = models.FloatField()
    bitcoin = models.FloatField()


class Binance_Candle(models.Model):
    high_price = models.FloatField()
    low_price = models.FloatField()

class Exchange(models.Model):
    usd_krw = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)