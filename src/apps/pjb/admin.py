from django.contrib import admin
from .models import *

class EdicaoPjbAdmin(admin.ModelAdmin):
    list_display = ['nome']
    ordering = ['nome']

class ComissaoPjbAdmin(admin.ModelAdmin):
    list_display = ['edicao_pjb', 'nome', 'sigla']
    ordering = ['edicao_pjb', 'nome']

class DeputadoPjbAdmin(admin.ModelAdmin):
    list_display = ['edicao_pjb', 'nome', 'data_nascimento', 'escola', 'serie', 'uf']
    ordering = ['edicao_pjb', 'nome']

class ProjetoPjbAdmin(admin.ModelAdmin):
    list_display = ['edicao_pjb', 'numero', 'ementa', 'entenda_a_proposta']
    ordering = ['edicao_pjb', 'numero']

admin.site.register(EdicaoPjb, EdicaoPjbAdmin)
admin.site.register(ComissaoPjb, ComissaoPjbAdmin)
admin.site.register(DeputadoPjb, DeputadoPjbAdmin)
admin.site.register(ProjetoPjb, ProjetoPjbAdmin)
