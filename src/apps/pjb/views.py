from django.shortcuts import render
from apps.pjb.models import DeputadoPjb, ProjetoPjb, ComissaoPjb, PartidoPjb, MesaDiretoraPjb
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

    def get_partido_obj(deputado):
        obj = None
        partidos = PartidoPjb.objects.filter(integrantes__id__in=[deputado.id]).order_by('nome')
        partido = partidos[0] if len(partidos) > 0 else None
        atribuicao = "Integrante" if partido else None
        if atribuicao:
            atribuicao = "Líder" if partido.lider == deputado else atribuicao
            atribuicao = "Primeiro(a) Vice-líder" if partido.primeiro_vice_lider == deputado else atribuicao
            atribuicao = "Segundo(a) Vice-líder" if partido.segundo_vice_lider == deputado else atribuicao
            atribuicao = "Terceiro(a) Vice-líder" if partido.terceiro_vice_lider == deputado else atribuicao
            atribuicao = "Quarto(a) Vice-líder" if partido.quarto_vice_lider == deputado else atribuicao
            atribuicao = f"{atribuicao} do {partido.nome}"
            obj = {"partido": partido, "atribuicao": atribuicao}
        return obj

    def get_comissoes_obj(deputado):
        obj = []
        comissoes = ComissaoPjb.objects.filter(integrantes__id__in=[deputado.id]).order_by('nome')
        for comissao in comissoes:
            atribuicao = "Integrante"
            atribuicao = "Presidente" if comissao.presidente == deputado else atribuicao
            atribuicao = "Vice presidente" if comissao.vice_presidente == deputado else atribuicao
            atribuicao = f"{atribuicao} da {comissao.nome}"
            obj.append({"comissao": comissao, "atribuicao": atribuicao})
        return obj

    def get_mesa_diretora_obj(deputado):
        obj = []
        mesas = MesaDiretoraPjb.objects.all()
        for mesa in mesas:
            atribuicao = None
            if mesa.presidente == deputado:
                atribuicao = "Presidente"
            if mesa.vice_presidente == deputado:
                atribuicao = "Vice presidente"
            if mesa.primeiro_secretario == deputado:
                atribuicao = "Primeiro(a) secretário(a)"
            if mesa.segundo_secretario == deputado:
                atribuicao = "Segundo(a) secretário(a)"
            if atribuicao:
                atribuicao = f"{atribuicao} da Mesa Diretora"
                obj.append({"mesa": mesa, "atribuicao": atribuicao})
        return obj

    comissoes = get_comissoes_obj(deputado)
    partido_obj = get_partido_obj(deputado)
    mesa = get_mesa_diretora_obj(deputado)
    return render(request, 'deputados-detail.html', {"deputado": deputado,
                                                     "projeto": projeto,
                                                     "comissoes": comissoes,
                                                     "partido": partido_obj,
                                                     "mesas": mesa,
                                                    })


def projeto_list_view(request):
    projetos = ProjetoPjb.objects.extra(
        select={'numero_convertido': 'CAST(numero AS INTEGER)'}
    ).order_by('numero_convertido').order_by('numero')

    return render(request, 'projetos-list.html', {"projetos": projetos})


def partido_detail_view(request, id):
    partido = get_object_or_404(PartidoPjb, pk=id)
    integrantes = partido.integrantes.all().order_by('nome')
    return render(request, 'partidos-detail.html', {
        "partido": partido,
        "integrantes": integrantes
    })


def partido_list_view(request):
    partidos = PartidoPjb.objects.all().order_by('nome')
    return render(request, 'partidos-list.html', {"partidos": partidos})


def projeto_detail_view(request, id):
    projeto = get_object_or_404(ProjetoPjb, pk=id)
    return render(request, 'projetos-detail.html', {"projeto": projeto})


def comissao_list_view(request):
    comissoes = ComissaoPjb.objects.all().order_by('nome')
    return render(request, 'comissoes-list.html', {"comissoes": comissoes})


def mesa_diretora_view(request):
    mesa = MesaDiretoraPjb.objects.all()
    mesa = mesa[0]
    integrantes = [mesa.presidente, mesa.vice_presidente, mesa.primeiro_secretario, mesa.segundo_secretario]
    return render(request, 'mesa-diretora.html', {"mesa": mesa, "integrantes": integrantes})


def comissao_detail_view(request, id):
    bills = get_wikilegis_index_data_no_randomness(200)
    comissao = get_object_or_404(ComissaoPjb, pk=id)
    integrantes = comissao.integrantes.all().order_by('nome')
    projetos = ProjetoPjb.objects.filter(autor__in=integrantes).extra(
        select={'numerointeger': 'CAST(numero AS INTEGER)'}).order_by('numerointeger').values()
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
