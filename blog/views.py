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


def about(request):
    about_msg = 'ABOUT ME'
    context = {
        'about_msg': about_msg,
    }
    return render(request, 'blog/about.html', context=context)


def categories(request):
    # всего категорий
    categories_count = Category.objects.all().count()
    # множество всех категорий
    categories = Category.objects.all()

    context = {
        'title': 'Все категории',
        'categories_count': categories_count,
        'categories': categories,
    }
    return render(request, 'blog/categories.html', context=context)


def add_post(request):
    context = {

    }
    return HttpResponse("Добавить пост")


def login(request):
    context = {

    }
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    post = Post.objects.filter(id=post_id)
    #new = post.values_list('title', 'author_id', 'author', 'content',)
    context = {
        'post': post,
    }
    return render(request, 'blog/post.html', context=context)
    # return HttpResponse(f"Отображение поста с id = {post_id}")


def show_category(request, cat_id):
    posts = Post.objects.filter(category_id=cat_id)
    current_cat = posts[0].category
    context = {
        'posts': posts,
        'cat_selected': cat_id,
        'current_cat': current_cat,
    }
    return render(request, 'blog/posts_by_category.html', context=context)


def pagenotfound(request, exception):
    """ Отображение страницы ошибки в случае перехода на несуществующую страницу
     в режиме DEBUG=False"""
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
