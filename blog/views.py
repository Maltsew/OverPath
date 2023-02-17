from django.shortcuts import render
from django.contrib.auth.models import User
from blog.models import Post, Category
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, Http404, HttpResponse


def homepage(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/homepage.html', context=context)


def base(request):
    context = {}
    return render(request, 'blog/post.html', context=context)


def about(request):
    about_msg = 'ABOUT ME'
    context = {
        'about_msg': about_msg,
    }
    return render(request, 'blog/about.html', context=context)


def categories(request):
    context = {

    }
    return HttpResponse("Категории")


def add_post(request):
    context = {

    }
    return HttpResponse("Добавить пост")


def login(request):
    context = {

    }
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    context = {

    }
    return HttpResponse(f"Отображение статьи с id = {post_id}")


def pagenotfound(request, exception):
    """ Отображение страницы ошибки в случае перехода на несуществующую страницу
     в режиме DEBUG=False"""
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
