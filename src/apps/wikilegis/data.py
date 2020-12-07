from django.conf import settings
import requests


def get_wikilegis_index_data(limit):
    url = settings.WIKILEGIS_UPSTREAM + '/api/v1/bill/'
    params = {'limit': '100'}
    response = requests.get(url, params=params)
    bills = response.json()['objects']
    print(bills)
    return bills
