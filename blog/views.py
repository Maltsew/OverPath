import random
import string

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from blog.models import Post, Tag, Profile
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.forms import modelformset_factory
from .forms import PostForm, ProfileRegistrationForm, ProfileLoginForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm


class ShowHomepage(ListView):
    paginate_by = 4
    model = Post
    template_name = 'blog/homepage.html'
    context_object_name = 'posts'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # временно - показ 3 последних постов
        context['preview_posts'] = Post.objects.all()[:3]
        return context


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


# class AddPost(LoginRequiredMixin, CreateView):
#     form_class = PostForm
#     template_name = 'blog/add_post.html'

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.save(commit=False)
            post_form.instance.author = request.user
            post_form.save()
            messages.success(request, 'Опубликовано')
            return redirect('homepage')
        else:
            messages.error(request, 'Ошибка публикации')
    else:
        post_form = PostForm()
    return render(request, 'blog/add_post.html', context={'form': post_form})

# class RegisterProfile(CreateView):
#     form_class = ProfileRegistrationForm
#     template_name = 'blog/profile_register.html'
#     success_url = reverse_lazy('login')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


def register(response):
    if response.method == 'POST':
        form = ProfileRegistrationForm(response.POST, response.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.about_user = form.cleaned_data.get('about_user')
            user.profile.profile_image = form.cleaned_data.get('profile_image')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=password)
            #login(response, user)

            return redirect('login')
    else:
        form = ProfileRegistrationForm()
    return render(response, 'blog/profile_register.html', {'form': form})


class LoginProfile(LoginView):
    form_class = ProfileLoginForm
    template_name = 'blog/login.html'

    def get_success_url(self):
        return reverse_lazy('homepage')


def profile_logout(request):
    logout(request)
    return redirect('login')


def pagenotfound(request, exception):
    """ Отображение страницы ошибки в случае перехода на несуществующую страницу
     в режиме DEBUG=False"""
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
