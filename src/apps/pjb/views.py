from django.shortcuts import render
from apps.pjb.models import DeputadoPjb, ProjetoPjb, ComissaoPjb
from django.shortcuts import get_object_or_404
from apps.wikilegis.data import get_wikilegis_index_data_no_randomness


def deputado_list_view(request):
    deputados = DeputadoPjb.objects.all().order_by('nome')
    return render(request, 'deputados-list.html', {"deputados": deputados})


def deputado_detail_view(request, id):
    deputado = get_object_or_404(DeputadoPjb, pk=id)
    try:
        projeto = ProjetoPjb.objects.get(autor_id=id)
    except ProjetoPjb.DoesNotExist:
        projeto = None

    try:
        comissao = ComissaoPjb.objects.get(integrantes__id__in=[deputado.id])
    except ComissaoPjb.DoesNotExist:
        comissao = None

    return render(request, 'deputados-detail.html', {"deputado": deputado,
                                                     "projeto": projeto,
                                                     "comissao": comissao})


def projeto_list_view(request):
    projetos = ProjetoPjb.objects.extra(
        select={'numero_convertido': 'CAST(numero AS INTEGER)'}
    ).order_by('numero_convertido')

    return render(request, 'projetos-list.html', {"projetos": projetos})


def projeto_detail_view(request, id):
    projeto = get_object_or_404(ProjetoPjb, pk=id)
    return render(request, 'projetos-detail.html', {"projeto": projeto})


def comissao_list_view(request):
    comissoes = ComissaoPjb.objects.all()
    return render(request, 'comissoes-list.html', {"comissoes": comissoes})


def comissao_detail_view(request, id):
    bills = get_wikilegis_index_data_no_randomness(200)
    comissao = get_object_or_404(ComissaoPjb, pk=id)
    integrantes = comissao.integrantes.all()
    projetos = ProjetoPjb.objects.filter(autor__in=integrantes).values()
    for bill in bills:
        tema = bill.get('theme').get('description')
        numero = bill['epigraph'].split('/')[0][-4:]
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
