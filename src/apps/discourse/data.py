from django.conf import settings
import requests
import random


def get_categories():
    categories_url = settings.DISCOURSE_UPSTREAM + '/categories.json'
    categories = requests.get(categories_url).json()
    categories = categories['category_list']['categories']
    return categories


def get_latest():
    latest_url = settings.DISCOURSE_UPSTREAM + '/latest.json'
    latest = requests.get(latest_url).json()
    latest = latest['topic_list']['topics']
    return latest


def get_discourse_index_data(amount):
    categories = get_categories()
    latest = get_latest()
    randomly_selected_latest = random.sample(latest, amount)

    topics = []
    for topic in randomly_selected_latest:
        topic_category = None

        for category in categories:
            subcategories = category.get('subcategory_ids', [])
            if category['id'] == topic['category_id']:
                topic_category = category
            elif topic['category_id'] in subcategories:
                topic_category = category

        topic['category_name'] = topic_category['name']
        topic['category_slug'] = topic_category['slug']

        topics.append(topic)

    return topics
