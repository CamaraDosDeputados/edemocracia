import random
from django.conf import settings
from revproxy.views import DiazoProxyView
from django.shortcuts import render
import json

from apps.discourse.data import get_discourse_index_data
from apps.wikilegis.data import get_wikilegis_index_data
from apps.pautas.data import get_pautas_index_data
from apps.audiencias.data import get_audiencias_index_data
from apps.core.utils import get_user_data

from apps.pjb.models import DeputadoPjb, ProjetoPjb


class EdemProxyView(DiazoProxyView):
    html5 = True

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        if request.user.is_authenticated:
            user_data = get_user_data(request.user)
            request.META['HTTP_REMOTE_USER_DATA'] = json.dumps(user_data)

        return super(EdemProxyView, self).dispatch(request, *args, **kwargs)


def index(request):
    context = {}
    if settings.PAUTAS_ENABLED:
        context['pautas'] = get_pautas_index_data()

    if settings.WIKILEGIS_ENABLED:
        context['bills'] = get_wikilegis_index_data()

    if settings.DISCOURSE_ENABLED:
        context['topics'] = get_discourse_index_data(6)

    if settings.AUDIENCIAS_ENABLED:
        rooms = get_audiencias_index_data()

        context['history_rooms'] = rooms['history_rooms']
        context['agenda_rooms'] = rooms['agenda_rooms']
        context['live_rooms'] = rooms['live_rooms']

    def get_random_records(model, amount):
        ids = model.objects.all().values_list('id', flat=True)
        random_ids = random.sample(list(ids), min(len(ids), amount))
        return model.objects.filter(id__in=random_ids)

    context['deputados'] = get_random_records(DeputadoPjb, 6)
    context['projetos'] = get_random_records(ProjetoPjb, 6)

    return render(request, 'index.html', context)
