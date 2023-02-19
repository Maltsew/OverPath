"""WasHere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from blog.views import homepage, base, about, categories, add_post, login, show_post, show_category


urlpatterns = [
    path('', homepage, name='homepage'),
    path('posts/', base, name='posts'),
    path('about/', about, name='about'),
    path('categories/', categories, name='categories'),
    path('add_post/', add_post, name='add_post'),
    path('login/', login, name='login'),
    path('show_post/<int:post_id>/', show_post, name='show_post'),
    path('category/<int:cat_id>/', show_category, name='show_category'),
]
