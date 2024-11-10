from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.template.loader import render_to_string

from .models import Women, Category, TagPost

menu = [{'title': "Про сайт", 'url_name': 'about'},
        {'title': "Додати статью", 'url_name': 'add_page'},
        {'title': "Зворотній звязок", 'url_name': 'contact'},
        {'title': "Увійти", 'url_name': 'login'}
]


def index(request):
    posts = Women.published.all().select_related('cat')

    date = {
        'title': 'Головна сторінка',
        'menu': menu,
        'float': 29.32,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', context=date)


def about(request):
    return render(request, 'women/about.html', {'title': 'Про сайт',  'menu': menu})


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'women/post.html', data)


def addpage(request):
    return HttpResponse(f"Додати статю")


def contac(request):
    return HttpResponse(f"Зворотній звязок")


def login(request):
    return HttpResponse(f"Авторизація")

def show_category(request, cat_id):
    return index(request)

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')
    date = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', context=date)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не знайдена</h1>")

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
    date = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=date)