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
from django.utils.text import slugify


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

# Перевод слагов на латиницу
from transliterate import translit, get_available_language_codes

from django.db.models import Q


class ShowHomepage(ListView):
    paginate_by = 4
    model = Post
    template_name = 'blog/homepage.html'
    context_object_name = 'posts'
    # allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # определяет контекст последних постов
        # в templatetags определен пользовательский тэг для такой же задачи
        # TO-DO пересмотреть функционал
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
    """ Функция добавления нового поста
    Автором поста назначается профиль, авторизованный в данный момент на сайте
    Поле slug: см. метод save() модели Post
    Поле категории поста являяются обязательным к заполнению
    Тэги поста добавляются к посту после его фактического сохранения в модель
    После заполнения всех полей, кроме поля категории поста, пост сохранется в модель (первичное сохранение)
    Первичное сохранение необходимо, чтобы в модели Post на момент добавления тэгов уже существовал пост
    с post_id, к которому после будут добавлены тэги.
    Тэги поста: тэги поста задаются в виде строки. Тэги разделяются запчтой, если тэгов больше одного
    После первичного сохранения поста, тэги, полученные с формы, сохраняются в список тэгов
    Для каждого тэга в списке тегов создается слаг тэга, аналогично созданию слага поста (
    название тэга переводится на латиницу и вызывается функция slugify)
    Для пары тэг: слаг_тэга создаетя словарь тэгов post_full_tags. Для ключей словаря вызывается
    get_or_create для модели Tag. В случает, если тэг уже существует, возвращает True.
    Если тэга не существовала, он создается в модели Tag.
    Конечным этапом является добавление данного тэга (или тэгов) к посту
    После происходит окончательное сохранение поста
    """
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post = post_form.save()
            post_tags = post_form.cleaned_data['tags'].split(', ') #list с тэгами из формы
            # для каждого тэга в списке post_tags
            post_full_tags = dict()
            for i in post_tags:
                # генерирование слага по названию, предварительно переводя его с кириллицы на латиницу
                slug_string = slugify(translit(i, 'ru', reversed=True), allow_unicode=True)
                # добавление в словарь пару 'тэг': 'тэг_слаг'
                post_full_tags[i] = slug_string
            # для каждого тэга из словаря с парами 'тэг': 'тэг_слаг' - получить (или создать) queryset из Tag
            for tag in post_full_tags:
                Tag.objects.get_or_create(title=tag, slug=post_full_tags[tag])
                post.tags.add(Tag.objects.get(title=tag, slug=post_full_tags[tag]))
            # Сохранение поста
            post.save()
            # messages.success(request, 'Опубликовано')
            return redirect('homepage')
        else:
            messages.error(request, 'Ошибка публикации')
    else:
        post_form = PostForm()
    return render(request, 'blog/add_post.html', context={'form': post_form})


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


# def search_post_by_title(request):
#     queryset = Post.objects.all()
#     query = request.GET.get('q')
#     if query:
#         queryset = queryset.filter(
#             Q(title__icontains=query)
#         )
#     context = {
#         'queryset': queryset
#     }
#     return render(request, 'blog/search.html', context)

# def get_empty_queryset():
#     return []


class Search(ListView):

    """ Поиск постов по названию.
    Логака поиска:
        если поисковой запррс пуст - возвращет сообщение об ошибке пустого запроса
        если поисковой запрос не пуст, но в модели Post нет ни одного совпадения по содержанию в названии -
        поднимает 404 на стриницу homepage
        если запрос не пуст и совпадения в модели найдены - показвает пост (посты)"""

    template_name = 'blog/homepage.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        empty_query_set = []
        if self.request.GET.get('q'):
            return Post.objects.filter(title__icontains=self.request.GET.get('q'))
        #raise Http404
        # если в запрос GET.get не передано значение по ключу q, возвращет пустой queryset
        return []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        # если контекст 'posts' это пустой queryset, дает исключение на домашнюю страницу о пустом запросе
        if context['posts'] == []:
            print('empty posts')
            raise Http404
        if context['posts'].count() == 0:
            print('no post return')
            raise Http404
        return context


def pagenotfound(request, exception):
    """ Отображение страницы ошибки в случае перехода на несуществующую страницу
     в режиме DEBUG=False"""
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
