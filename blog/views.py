from django.shortcuts import render
from django.contrib.auth.models import User
from blog.models import Post, Category
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, Http404


# Create your views here.
menu = ['Main', 'About', 'Categories']


def base(request):
    context = {}
    return render(request, 'layout/base.html', context=context)


def homepage(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'menu': menu,
    }
    return render(request, 'blog/homepage.html', context=context)


def about(request):
    about_msg = 'ABOUT ME'
    context = {
        'about_msg': about_msg,
    }
    return render(request, 'blog/about.html', context=context)


def pagenotfound(request, exception):
    """ Отображение страницы ошибки в случае перехода на несуществующую страницу
     в режиме DEBUG=False"""
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
