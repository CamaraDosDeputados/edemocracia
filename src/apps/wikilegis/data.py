from django.conf import settings
import requests
import random


def get_wikilegis_index_data(limit):
    url = settings.WIKILEGIS_UPSTREAM + '/api/v1/bill/'
    params = {'limit': '100'}
    response = requests.get(url, params=params)
    bills = response.json()['objects']
    randomly_selected_bills = random.sample(bills, limit)

    return randomly_selected_bills
