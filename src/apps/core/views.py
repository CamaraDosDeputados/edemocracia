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
    records_limit = 6
    context = {}
    if settings.PAUTAS_ENABLED:
        context['pautas'] = get_pautas_index_data()

    if settings.WIKILEGIS_ENABLED:
        context['bills'] = get_wikilegis_index_data(records_limit)

    if settings.DISCOURSE_ENABLED:
        def include_pictures_in_discourse(topics):
            for topic in topics:
                full_name = str(topic['title']).split('-')[0].split(' ')
                full_name = [x for x in full_name if x != '']
                last_name = full_name[len(full_name)-1]
                query = DeputadoPjb.objects.filter(nome__icontains=last_name)
                if len(query) > 1:
                    first_name = full_name[0]
                    query = DeputadoPjb.objects.filter(nome__icontains=first_name)
                if len(query) > 0:
                    try:
                        topic['foto'] = query[0].foto
                    except:
                        pass
        context['topics'] = get_discourse_index_data(records_limit)
        include_pictures_in_discourse(context['topics'])

    if settings.AUDIENCIAS_ENABLED:
        rooms = get_audiencias_index_data()

        context['history_rooms'] = rooms['history_rooms']
        context['agenda_rooms'] = rooms['agenda_rooms']
        context['live_rooms'] = rooms['live_rooms']

    def get_random_records(model, amount):
        ids = model.objects.all().values_list('id', flat=True)
        random_ids = random.sample(list(ids), min(len(ids), amount))
        return model.objects.filter(id__in=random_ids)

    context['deputados'] = get_random_records(DeputadoPjb, records_limit)
    context['projetos'] = get_random_records(ProjetoPjb, records_limit)

    return render(request, 'index.html', context)
