from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin


class WomenHome(DataMixin, ListView):
    # model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Головна сторінка'
    cat_selected = 0


    def get_queryset(self):
        return Women.published.all().select_related('cat')


def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html',
                  {'title': 'Про сайт', 'page_obj': page_obj})


class ShowPost(DataMixin, DetailView):
    # model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Додавання статі'


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ['title',  'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home') #функція будуэ маршрут тільки в той момент, коли до даної сторінки звертаються
    title_page = 'Редагування статі'


def contact(request):
    return HttpResponse(f"Зворотній звязок")


def login(request):
    return HttpResponse(f"Авторизація")


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False


    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категорія - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не знайдена</h1>")


class TagPostlist(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)
