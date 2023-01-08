import requests
from django.core.management.base import BaseCommand, CommandError
from main.models import Currency, MainTrade

class Command(BaseCommand):
    def handle(self, *args, **options):

        r = requests.get('https://www.kucoin.com/_api_kumex/kumex-contract/contracts/active')
        r = r.json()['data']
        print(r)
        for item in Currency.objects.all():
            item.delete()

        for item in r:
            if not len(Currency.objects.filter(brand = item['baseCurrency'])):
                c = Currency(name = item['baseCurrency'], brand= item['baseCurrency'],)
                c.save()
            if not len(Currency.objects.filter(brand = item['quoteCurrency'])):
                c = Currency(name = item['quoteCurrency'], brand= item['quoteCurrency'],)
                c.save()
        
        for item in MainTrade.objects.all():
            item.delete()

        for item in r:
            if not len(MainTrade.objects.filter(bcurrency = Currency.objects.get(brand = item['baseCurrency']),scurrency = Currency.objects.get(brand = item['quoteCurrency']))):
                c = MainTrade(name= item['baseCurrency'] + ' PERP', bcurrency = Currency.objects.get(brand = item['baseCurrency']),scurrency = Currency.objects.get(brand = item['quoteCurrency']), brand = item['symbol'])
                c.save()