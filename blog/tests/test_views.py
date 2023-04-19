from django.test import TestCase, Client
from django.contrib.auth.models import User
from blog.models import Post, Tag
from django.urls import reverse
from unittest import skip
from blog.views import create_tags_from_list


""" Тесты views для приложения blog"""


class BlogPagesTests(TestCase):
    """ Тесты на соотв. отображения страниц их URL-адресам для приложения blog"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # создание автора (создателя постов)
        cls.user = User.objects.create_user(username='IvanovIvan', first_name='Ivan', last_name='Ivanov',
                            email='ivanov@gmail.com')
        # Создание пользователя (как посетителя)
        cls.viewer = Client()
        # авторизации для автора
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        # Создание записи поста в БД
        cls.post = Post.objects.create(title='Test Title', author=cls.user, content='Test post content')

    def test_homepage_uses_correct_template(self):
        """ Домашнаяя страница использует соотв. шаблон"""
        response = self.viewer.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'blog/homepage.html')

    def test_homepage_authorized_users(self):
        """ Домашняя страница для авторизованного польз."""
        response = self.authorized_client.get(reverse('homepage'))
        self.assertTemplateUsed(response, 'blog/homepage.html')

    def test_add_post_uses_correct_template(self):
        """ Страница создания поста Создание постов доступно только авторизованным"""
        response = self.authorized_client.get(reverse('add_post'))
        self.assertTemplateUsed(response, 'blog/add_post.html')

    def test_add_post_allow_only_authorized(self):
        """ Создание постов доступно только авторизованным"""
        response = self.authorized_client.get(reverse('add_post'))
        self.assertEqual(response.status_code, 200)

    def test_add_post_redirects_for_unauthorized(self):
        """ Создание постов недоступно для viewers, т.к.
        view create_post использует @login_required, который перенаправляет на стриницу login"""
        response = self.viewer.get(reverse('add_post'))
        self.assertEqual(response.status_code, 302)

    def test_tags_uses_correct_template(self):
        """ Отображение всех тэгов использует соотв. шаблон"""
        response = self.viewer.get(reverse('tags'))
        self.assertTemplateUsed(response, 'blog/tags.html')

    def test_show_post_uses_correct_template(self):
        """ Просмотр поста использует соотв. шаблон"""
        post = BlogPagesTests.post
        response = self.viewer.get(reverse('post', kwargs={'post_slug': post.slug}))
        self.assertTemplateUsed(response, 'blog/post.html')

    def test_posts_by_tags_uses_correct_template(self):
        """ Отображение всех постов по выбранному тэгу использует соотв. шаблон
        post_by_tags template"""
        post = BlogPagesTests.post
        # создание тэга
        tag = Tag.objects.create(title='Тест', slug='test')
        # добавление его к посту
        post.tags.add(tag)
        response = self.viewer.get(reverse('tag', kwargs={'tag_slug': tag.slug}))
        self.assertTemplateUsed(response, 'blog/posts_by_tags.html')

    @skip
    def test_posts_by_tags_redirect_to_current_post(self):
        """ после выбора определенной категории - отображение всех постов,
        содержащих данную категорию"""
        pass

    def test_add_post_uses_correct_template(self):
        """ Создание поста использует соотв. шаблон"""
        response = self.authorized_client.get(reverse('add_post'))
        self.assertTemplateUsed(response, 'blog/add_post.html')

    def test_test_login_uses_correct_template(self):
        """ Login использует соотв. шаблон"""
        response = self.viewer.get(reverse('login'))
        self.assertTemplateUsed(response, 'blog/login.html')

    def test_logout_uses_correct_template(self):
        """ Logout реализован с помощью логики logout(request),
        поэтому необходимо проверять редирект на страницу login"""
        response = self.authorized_client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    @skip
    def test_search_uses_correct_template(self):
        """ Поиск использует соотв. шаблон
        Поиск доступен только авторизованным польз.
        Пробуем найти название поста"""
        # TODO после добавления LoginRequiredMixin логику теста надо пересмотреть
        post = BlogPagesTests.post
        url = '{url}?{filter}={value}'.format(
            url=reverse('search'),
            filter='q',
            value=post.title
        )
        response = self.authorized_clie.get(url)
        self.assertTemplateUsed(response, 'blog/homepage.html')

    def test_empty_search_uses_404(self):
        """ Пустой поисковой запрос отправляет на 404"""
        response = self.authorized_client.get(reverse('search'))
        self.assertEqual(response.status_code, 404)

    def test_search_forbidden_for_unauthorized(self):
        """ Поисковой запрос, введенный напрямую в параметры URL,
        должен быть недоступен для неавторизованного пользователя
        """
        post = BlogPagesTests.post
        url = '{url}?{filter}={value}'.format(
            url=reverse('search'),
            filter='q',
            value=post.title
        )
        response = self.viewer.get(url)
        self.assertEqual(response.status_code, 302)

    def test_create_tags_from_valid_tags_string(self):
        """ Функция преобразования строки с тэгами из формы создания поста
        преобразует тэги в словарь 'tag': 'tag_slug' """
        valid_tag_string = "Проверка,тестовый тэг,новый тэг"
        # преобразование в список как в create_post
        valid_tag_list = valid_tag_string.split(',')
        get_tags = create_tags_from_list(valid_tag_list)
        expected_tags_dict = {'Проверка': 'proverka', 'тестовый тэг': 'testovyj-teg', 'новый тэг': 'novyj-teg'}
        self.assertEqual(expected_tags_dict, get_tags)
