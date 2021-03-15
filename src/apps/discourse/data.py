from django.conf import settings
import requests


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


def get_posts(id):
    latest_url = settings.DISCOURSE_UPSTREAM + f'/t/{id}/posts.json'
    latest = requests.get(latest_url).json()
    latest = latest['post_stream']['posts']
    return latest


def get_topic(id):
    latest_url = settings.DISCOURSE_UPSTREAM + f'/t/{id}.json'
    latest = requests.get(latest_url).json()
    return latest


def get_index_data(topics_list):
    categories = get_categories()
    topics = []
    for topic in topics_list:
        topic_category = None
        for category in categories:
            subcategories = category.get('subcategory_ids', [])
            print(category, topic)
            if category['id'] == topic['category_id']:
                topic_category = category
            elif topic['category_id'] in subcategories:
                topic_category = category

        topic['category_name'] = topic_category['name']
        topic['category_slug'] = topic_category['slug']

        topics.append(topic)

    return topics


def get_discourse_index_data(id_list=[]):
    if len(id_list) == 0:
        return get_index_data(get_latest())
    topics = []
    for id in id_list:
        topics.append(get_topic(id))
    return get_index_data(topics)
