from binance.client import Client
import time, os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
django.setup()

from btc.models import Order, ClosedOrder,Wallet, Binance_Candle
from django.contrib.auth import get_user_model


API_key= 'nu1AV1q04nvVCGcZpxmYYM4AJovxghU644sTP5Q59Xo4T5tjwsBwLEp4viXQU4om'
Secret_key = 'yruAAb0iJ1mwz8hsxVIrklph4YWW82Uhb1vlPdiQ1pNMV9EJWOjV1MY0UPHPp7ev'

client = Client(API_key, Secret_key)



while True :
    order_list = Order.objects.all()
    candle = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "5 minute ago UTC")

    high = float(candle[0][2])
    low = float(candle[0][3])
    bc = Binance_Candle.objects.get(pk=1)
    bc.high_price = round(high, 2)
    bc.low_price = round(low, 2)
    bc.save()
    print(high,low)


    for order in order_list:
        if order.position == 'buy':
            if order.order_price >= high :
                new_closed_order = ClosedOrder.objects.create(
                    user=order.user,
                    closed_price=order.order_price,
                    amount=order.amount,
                    deposit=order.deposit,
                    position=order.position)
                new_closed_order.save()
                wallet = Wallet.objects.get(user_id=order.user_id)
                if wallet.bitcoin != 0:
                    wallet.average_price = round((wallet.average_price * wallet.bitcoin + \
                                                 order.order_price * order.amount) / (wallet.bitcoin + order.amount), 2)

                    wallet.bitcoin += order.amount
                    order.delete()
                    print('주문 체결')
                    wallet.save()
                    print('주문 체결')
                else:
                    wallet.average_price = order.order_price
                    wallet.bitcoin += order.amount
                    print('주문 체결')
                    wallet.save()
                    order.delete()
                    print('주문 체결')
        else : # sell
            if order.order_price <= low :
                new_closed_order = ClosedOrder.objects.create(
                    user=order.user,
                    closed_price=order.order_price,
                    amount=order.amount,
                    deposit=order.deposit,
                    position=order.position)
                new_closed_order.save()
                wallet = Wallet.objects.get(user_id=order.user_id)
                order_user = get_user_model().objects.get(pk=wallet.user_id)
                if (wallet.bitcoin - order.amount) <= 0.001:
                    order_user.usdt += order.deposit
                    order_user.save()
                    wallet.average_price = 0
                    wallet.bitcoin = 0
                    wallet.save()
                    order.delete()
                else:
                    order_user.usdt += order.deposit
                    order_user.save()
                    wallet.bitcoin -= order.amount
                    wallet.save()
                    order.delete()
    time.sleep(300)