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
from blog.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', ShowHomepage.as_view(), name='homepage'),
    path('about/', about, name='about'),
    path('tags/', tags, name='tags'),
    path('add_post/', create_post, name='add_post'),
    path('register/', register, name='register'),
    path('login/', LoginProfile.as_view(), name='login'),
    path('logout/', profile_logout, name='logout'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('tag/<slug:tag_slug>/', BlogTags.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
