from django.contrib import admin
from .models import *

class EdicaoPjbAdmin(admin.ModelAdmin):
    list_display = ['nome']
    ordering = ['nome']

class ComissaoPjbAdmin(admin.ModelAdmin):
    list_display = ['edicao_pjb', 'nome', 'sigla']
    list_display_links = ['nome', ]
    ordering = ['edicao_pjb', 'nome']

class DeputadoPjbAdmin(admin.ModelAdmin):
    list_display = ['edicao_pjb', 'nome', 'data_nascimento', 'escola', 'serie', 'uf']
    list_display_links = ['nome', ]
    ordering = ['edicao_pjb', 'nome']

class ProjetoPjbAdmin(admin.ModelAdmin):
    list_display = ['edicao_pjb', 'epigrafe', 'sigla_tipo', 'numero', 'ano', 'ementa', 'entenda_a_proposta']
    list_display_links = ['epigrafe', ]
    ordering = ['edicao_pjb', 'numero']

admin.site.register(EdicaoPjb, EdicaoPjbAdmin)
admin.site.register(ComissaoPjb, ComissaoPjbAdmin)
admin.site.register(DeputadoPjb, DeputadoPjbAdmin)
admin.site.register(ProjetoPjb, ProjetoPjbAdmin)
