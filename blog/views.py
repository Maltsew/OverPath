from django.shortcuts import render
from django.contrib.auth.models import User
from blog.models import Post, Category
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, Http404


# Create your views here.
menu = ['Main', 'About', 'Categories']


def homepage(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
        'menu': menu,
    }
    return render(request, 'blog/homepage.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')