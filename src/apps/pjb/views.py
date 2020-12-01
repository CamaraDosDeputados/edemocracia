from django.shortcuts import render
from apps.pjb.models import Escola
from django.shortcuts import get_object_or_404


def escola_list_view(request):
    escolas = Escola.objects.all()
    print(escolas)
    return render(request, 'escolas-list.html', {"escolas": escolas})


def escola_detail_view(request, id):
    escola = get_object_or_404(Escola, pk=id)
    return render(request, 'escolas-detail.html', {"escola": escola})
