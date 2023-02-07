from django.shortcuts import render
from django.contrib.auth.models import User
from blog.models import Post, Category


# Create your views here.
def homepage(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/homepage.html', context=context)


def by_category(request, category_id):
    posts = Post.objects.filter(categories=category_id)
    categories = Category.objects.all()
    current_category = Category.objects.get(pk=category_id)
    context = {
        'posts': posts,
        'categories': categories,
        'current_category': current_category,
    }
    return render(request, 'blog/by_category.html', context)
