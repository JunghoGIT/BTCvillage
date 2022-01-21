import requests
import json
import time, os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
django.setup()

from btc.models import Exchange

while True :
    res = requests.get("https://v6.exchangerate-api.com/v6/4e6f73e8174dbad71cc9ffb2/latest/USD")
    res_json = json.loads(res.content)
    exchange_rate = round(res_json["conversion_rates"]["KRW"],2)
    exchange = Exchange.objects.get(pk=1)
    exchange.usd_krw = exchange_rate
    exchange.save()
    time.sleep(7200)




