from django.shortcuts import render
from django.contrib.auth.models import User
from blog.models import Post, Category, Images, Profile
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, Http404, HttpResponse

from django.forms import modelformset_factory
from .forms import ImageForm, PostForm, CategoryForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


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


def categories(request):
    # всего категорий
    categories_count = Category.objects.all().count()
    context = {
        'title': 'Все категории',
        'categories_count': categories_count,
    }
    return render(request, 'blog/categories.html', context=context)


def login(request):
    context = {

    }
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    post = Post.objects.filter(id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'blog/post.html', context=context)


def show_category(request, cat_id):
    posts = Post.objects.filter(category_id=cat_id)
    current_cat = posts[0].category
    context = {
        'posts': posts,
        'cat_selected': cat_id,
        'current_cat': current_cat,
    }
    return render(request, 'blog/posts_by_category.html', context=context)


def add_post(request):
    pass


def pagenotfound(request, exception):
    """ Отображение страницы ошибки в случае перехода на несуществующую страницу
     в режиме DEBUG=False"""
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
