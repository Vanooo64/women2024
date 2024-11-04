from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.template.loader import render_to_string

menu = [{'title': "Про сайт", 'url_name': 'about'},
        {'title': "Додати статью", 'url_name': 'add_page'},
        {'title': "Зворотній звязок", 'url_name': 'contact'},
        {'title': "Увійти", 'url_name': 'login'}
]


data_db = [
    {'id': 1, 'title': 'Анджеліна Джолі', 'content': '''<h1>Анджеліна Джолі</h1> при народженні Войт (англ. Voight), раніше Джолі Пітт (англ. Jolie Pitt); рід. 4 червня 1975, Лос-Анджелес, Каліфорнія, США) - американська актриса кіно, телебачення та озвучування, кінорежисер, сценаристка, продюсер, фотомодель, посол доброї волі ООН.
 Володарка премії «Оскар», трьох премій «Золотий глобус» (перша актриса в історії, яка три роки поспіль виграла премію) та двох «Премій Гільдії кіноакторів США».''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робі', 'content': 'Біография Марго Робі', 'is_published': False},
    {'id': 3, 'title': 'Джулія Робертс', 'content': 'Біография Джулії Робертс', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Актрорки'},
    {'id': 2, 'name': 'Співачки'},
    {'id': 3, 'name': 'Спортсменки'},
]

def index(request):
    # t = render_to_string('women/index.html')
    # return HttpResponse(t)
    date = {
        'title': 'Головна сторінка',
        'menu': menu,
        'float': 29.32,
        'posts': data_db,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=date)


def about(request):
    return render(request, 'women/about.html', {'title': 'Про сайт',  'menu': menu})


def show_post(request):
    return HttpResponse(f"Відoбраження статі з id: {post_id}")


def addpage(request):
    return HttpResponse(f"Додати статю")


def contac(request):
    return HttpResponse(f"Зворотній звязок")


def login(request):
    return HttpResponse(f"Авторизація")

def show_category(request, cat_id):
    return index(request)

def show_category(request, cat_id):
    date = {
        'title': 'Відображення по рубрикам',
        'menu': menu,
        'float': 29.32,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'women/index.html', context=date)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не знайдена</h1>")