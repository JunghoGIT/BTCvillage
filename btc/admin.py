from django.contrib import admin
from .models import Order, Wallet, ClosedOrder,Binance_Candle, Exchange
# Register your models here.



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'order_price',
        'amount',
        'deposit',
        'position',
        'created_at'
    ]

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'average_price',
        'bitcoin',
    ]

@admin.register(ClosedOrder)
class ClosedOrderAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'closed_price',
        'amount',
        'deposit',
        'position',
        'created_at',

    ]

@admin.register(Binance_Candle)
class Binance_CandleAdmin(admin.ModelAdmin):
    list_display = [
        'high_price',
        'low_price',
    ]

@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = [
        'usd_krw',
        'updated_at',
    ]

