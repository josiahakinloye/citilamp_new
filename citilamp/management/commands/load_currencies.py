import requests, json
from django.core.management.base import BaseCommand

from citilamp.models import Country


class Command(BaseCommand):

    def handle(self, *args, **options):
        url = 'https://free.currencyconverterapi.com/api/v5/countries'
        response = requests.get(url).content
        response = json.loads(response.decode())
        counter = 0
        for key, item in response['results'].items():
            try:
                country = Country.objects.get(iso_alpha_2_code__iexact=key)
            except Country.DoesNotExist:
                print('Country not found with code', key)
                continue
            except Country.MultipleObjectsReturned:
                print('Multiple objects returned for', key)
                continue
            country.currency_code = item['currencyId']
            country.save()
            counter += 1
        print(counter, "countries updated")
