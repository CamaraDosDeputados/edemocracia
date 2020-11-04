from django.conf import settings


def settings_variables(request):
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
        'OLARK_ID': settings.OLARK_ID,
        'WIKILEGIS_ENABLED': settings.WIKILEGIS_ENABLED,
        'PAUTAS_ENABLED': settings.PAUTAS_ENABLED,
        'DISCOURSE_ENABLED': settings.DISCOURSE_ENABLED,
        'AUDIENCIAS_ENABLED': settings.AUDIENCIAS_ENABLED,
        'CAMARA_LOGIN': settings.CAMARA_LOGIN,
        'BASE_URL_EDEMOCRACIA': settings.BASE_URL_EDEMOCRACIA,
        'BASE_URL_WIKILEGIS': settings.BASE_URL_WIKILEGIS,
        'BASE_URL_PAUTAS': settings.BASE_URL_PAUTAS,
        'BASE_URL_AUDIENCIAS': settings.BASE_URL_AUDIENCIAS,
        'BASE_URL_DISCOURSE': settings.BASE_URL_DISCOURSE,
    }
