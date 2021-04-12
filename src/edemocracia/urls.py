from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from apps.accounts.api import api_root, UserListAPI
from apps.core.views import index
from apps.pjb.views import deputado_list_view, deputado_detail_view, \
     projeto_list_view, projeto_detail_view, comissao_detail_view, \
     comissao_list_view, mesa_diretora_view

base_url_edemocracia = settings.BASE_URL_EDEMOCRACIA.lstrip('/')

urlpatterns = [
    path(base_url_edemocracia + '', index, name='home'),
    path(base_url_edemocracia + 'deputado/list',
         deputado_list_view, name='deputado-list'),
    path(base_url_edemocracia + 'deputado/<int:id>/detail',
         deputado_detail_view, name='deputado-detail'),
    path(base_url_edemocracia + 'projeto/list',
         projeto_list_view, name='projeto-list'),
    path(base_url_edemocracia + 'projeto/<int:id>/detail',
         projeto_detail_view, name='projeto-detail'),
    path(base_url_edemocracia + 'comissao/<int:id>/detail',
         comissao_detail_view, name='comissao-detail'),
    path(base_url_edemocracia + 'comissao/list',
         comissao_list_view, name='comissao-list'),
    path(base_url_edemocracia + 'mesa-diretora',
         mesa_diretora_view, name='mesa-diretora'),
    path(base_url_edemocracia + 'admin/', admin.site.urls),
    path(base_url_edemocracia + 'accounts/', include('apps.accounts.urls')),
    path(base_url_edemocracia + 'sobre/', include('apps.about.urls')),
    path(base_url_edemocracia + 'api/v1/', api_root),
    path(base_url_edemocracia + 'api/v1/user/', UserListAPI.as_view(),
         name='user_list_api'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


if settings.WIKILEGIS_ENABLED:
    base_url_wikilegis = settings.BASE_URL_WIKILEGIS.lstrip('/')
    urlpatterns.append(path(base_url_wikilegis,
                            include('apps.wikilegis.urls')))

if settings.PAUTAS_ENABLED:
    base_url_pautas = settings.BASE_URL_PAUTAS.lstrip('/')
    urlpatterns.append(path(base_url_pautas, include('apps.pautas.urls')))

if settings.AUDIENCIAS_ENABLED:
    base_url_audiencias = settings.BASE_URL_AUDIENCIAS.lstrip('/')
    urlpatterns.append(path(base_url_audiencias,
                            include('apps.audiencias.urls')))


if settings.DISCOURSE_ENABLED:
    base_url_discourse = settings.BASE_URL_DISCOURSE.lstrip('/')
    urlpatterns.append(path(base_url_discourse,
                       include('apps.discourse.urls')))

admin.site.site_header = 'e-Democracia'
