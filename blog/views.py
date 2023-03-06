from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from blog.models import Post, Tag, Profile
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.forms import modelformset_factory
from .forms import PostForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def homepage(request):
    context = {
    }
    return render(request, 'blog/homepage.html', context=context)


def about(request):
    about_msg = 'ABOUT ME'
    context = {
        'about_msg': about_msg,
    }
    return render(request, 'blog/about.html', context=context)


def tags(request):
    # всего категорий
    context = {
        'title': 'Все тэги',
    }
    return render(request, 'blog/tags.html', context=context)


def login(request):
    context = {

    }
    return HttpResponse("Авторизация")


# def show_post(request, post_slug):
#     # надежнее, если нет постов вывод не пустого шаблона post, а страницы 404
#     post = get_object_or_404(Post, slug=post_slug)
#     context = {
#         'post': post,
#         'page_title': post.title,
#     }
#     return render(request, 'blog/post.html', context=context)


class ShowPost(DetailView):
    model = Post
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(slug=self.kwargs['post_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BlogTags(ListView):
    model = Post
    template_name = 'blog/posts_by_tags.html'
    context_object_name = 'posts'
    # Запрещает показывать пустые списки - для обработки перехода по несуществующему слагу
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['tag_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = context['posts'][0]
        context['tags'] = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return context


class AddPost(CreateView):
    form_class = PostForm
    template_name = 'blog/add_post.html'


# def add_post(request):
#     ''' при работе с формой, которая предусматривает загрузку файлов (в т.ч. изображений)
#     необхожимо учесть следующее:
#     в шаблоне, который использует форму. необходимо использовать enctype="multipart/form-data"
#     и при обработке запроса с формой учитывать данные из объекта request:
#     request.FILES'''
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post_slug = form.cleaned_data['slug']
#             form.save(commit=True)
#             return redirect('homepage')
#     else:
#         form = PostForm()
#     return render(request, 'blog/add_post.html', {'form': form})


def pagenotfound(request, exception):
    """ Отображение страницы ошибки в случае перехода на несуществующую страницу
     в режиме DEBUG=False"""
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
