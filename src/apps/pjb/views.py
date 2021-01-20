from django.shortcuts import render
from apps.pjb.models import DeputadoPjb, ProjetoPjb, ComissaoPjb
from django.shortcuts import get_object_or_404
from apps.wikilegis.data import get_wikilegis_index_data_no_randomness


def deputado_list_view(request):
    deputados = DeputadoPjb.objects.all().order_by('nome')
    return render(request, 'deputados-list.html', {"deputados": deputados})


def deputado_detail_view(request, id):
    # TODO: Vai falhar se um deputado puder ter mais de um projeto
    deputado = get_object_or_404(DeputadoPjb, pk=id)
    try:
        projeto = ProjetoPjb.objects.get(autor_id=id)
    except ProjetoPjb.DoesNotExist:
        projeto = None

    comissoes = ComissaoPjb.objects.filter(integrantes__id__in=[deputado.id]).order_by('nome')

    return render(request, 'deputados-detail.html', {"deputado": deputado,
                                                     "projeto": projeto,
                                                     "comissoes": comissoes})


def projeto_list_view(request):
    projetos = ProjetoPjb.objects.extra(
        select={'numero_convertido': 'CAST(numero AS INTEGER)'}
    ).order_by('numero_convertido').order_by('numero')

    return render(request, 'projetos-list.html', {"projetos": projetos})


def projeto_detail_view(request, id):
    projeto = get_object_or_404(ProjetoPjb, pk=id)
    return render(request, 'projetos-detail.html', {"projeto": projeto})


def comissao_list_view(request):
    comissoes = ComissaoPjb.objects.all().order_by('nome')
    return render(request, 'comissoes-list.html', {"comissoes": comissoes})


def comissao_detail_view(request, id):
    bills = get_wikilegis_index_data_no_randomness(200)
    comissao = get_object_or_404(ComissaoPjb, pk=id)
    integrantes = comissao.integrantes.all().order_by('nome')
    projetos = ProjetoPjb.objects.filter(autor__in=integrantes).values().order_by('numero')
    for bill in bills:
        tema = bill.get('description')
        numero = bill['epigraph'].split('/')[0][-3:]
        for projeto in projetos:
            try:
                n_projeto = int(projeto.get('numero'))
                numero = int(numero)
                if n_projeto == numero:
                    projeto['tema'] = tema
                    break
            except:
                pass

    return render(request, 'comissoes-detail.html',
                  {"comissao": comissao,
                   "propostas": projetos})
