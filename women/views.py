from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Сторінка додатку women')

def categories(request, cat_id):
    return HttpResponse(f'<h1>Статі по категоріям</h1><p>id: {cat_id}<p/>')
