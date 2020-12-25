from django.conf import settings
import requests
import random


def get_wikilegis_index_data_no_randomness(limit=100):
    url = settings.WIKILEGIS_UPSTREAM + '/api/v1/bill/'
    params = {'limit': '100'}
    response = requests.get(url, params=params)
    bills = response.json()['objects']
    return bills


def get_wikilegis_index_data(limit=100):
    bills = get_wikilegis_index_data_no_randomness(limit)
    randomly_selected_bills = random.sample(bills, limit)
    return randomly_selected_bills
