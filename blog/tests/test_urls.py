""" Тесты urls приложения blog
особенностью проверки доступности страниц является то, что в качестве аргумента response используется
непосредственно адрес машрута
"""
from django.test import TestCase, Client
from unittest import skip
from django.contrib.auth.models import User
from blog.models import Tag, Post


class StaticPagesURLTests(TestCase):
    """
    тестирование маршрутов статических страниц
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def test_about_page_status_OK(self):
        """
        Проверка доступности адреса about/
        """
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)


class BlogEmptyPagesURLsTests(TestCase):
    """
    Тестирование маршрутов тех страницы приложения блог, для которых Allow_Empty = False, то есть польз. видит страницу 404
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    @skip
    def test_empty_homepage_uses_404_template(self):
        """
        Если нет ни одного поста, домашняя страница отображает страницу 404
        """
        # TODO создать страницу 404
        response = self.guest_client.get('/')
        self.assertTemplateUsed(response, 'blog/404.html')

    def test_empty_homepage_status_404(self):
        """
        Если нет ни одного поста, домашняя страница возвращает 404
        """
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 404)

    @skip
    def test_empty_posts_by_tags_uses_404_template(self):
        """ Если нет ни одного тэга, страница отображения тэгов возвращает страницу 404"""
        # создаем тэг
        # TODO создать страницу 404
        tag = Tag.objects.create(title='Тест', slug='test')
        # по выбранному тэгу нет ни одного поста, должен возвращать страницу 404
        response = self.guest_client.get('tag/', kwargs={'tag_slug': tag.slug})
        self.assertTemplateUsed(response, 'blog/404.html')

    def test_empty_posts_by_tags_status_404(self):
        """
        Если нет ни одного поста, домашняя страница возвращает 404
        """
        tag = Tag.objects.create(title='Тест', slug='test')
        response = self.guest_client.get('tag/', kwargs={'tag_slug': tag.slug})
        self.assertEqual(response.status_code, 404)


class BlogURLsTests(TestCase):
    """
    Тестирование основных страниц приложения blog
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create(username='IvanovIvan', first_name='Ivan', last_name='Ivanov',
                                       email='ivanov@gmail.com')
        cls.tag = Tag.objects.create(title='Тест', slug='test')
        cls.post = Post.objects.create(title='Test Title', author=cls.user, content='Test post content')

        # авторизованный юзер
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_homepage_status_200(self):
        """
        Проверка доступности адреса homepage/ для неавторизованного пользователя
        """
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        """ Homepage страница использует корректный шаблон"""
        response = self.guest_client.get('/')
        self.assertTemplateUsed(response, 'blog/homepage.html')

    def test_tags_uses_correct_template(self):
        """ Tags использует корректный шаблон"""
        response = self.guest_client.get('/tags/')
        self.assertTemplateUsed(response, 'blog/tags.html')

    def test_add_post_uses_correct_template(self):
        """ Add Post пост использует корректный шаблон (доступно только авторизованным)"""
        response = self.authorized_client.get('/add_post/')
        self.assertTemplateUsed(response, 'blog/add_post.html')

    def test_register_uses_correct_template(self):
        """ register использует корректный шаблон"""
        response = self.guest_client.get('/register/')
        self.assertTemplateUsed(response, 'blog/profile_register.html')

    def test_login_uses_correct_template(self):
        """ login использует корректный шаблон"""
        response = self.guest_client.get('/login/')
        self.assertTemplateUsed(response, 'blog/login.html')

    def test_logout_uses_correct_template(self):
        """ logout пост использует корректный шаблон (редирект на логин) (доступно только авторизованным)"""
        response = self.authorized_client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_showpost_uses_correct_template(self):
        """ ShowPost использует корректный шаблон"""
        post = BlogURLsTests.post
        expected_absolute_url = '/post/' + post.slug + '/'
        response = self.authorized_client.get(expected_absolute_url)
        self.assertTemplateUsed(response, 'blog/post.html')

    def test_blogtags_uses_correct_template(self):
        """ BlogTags использует корректный шаблон"""
        # необходим какой либо тэг
        tag = BlogURLsTests.tag
        # необходим любой пост
        post = BlogURLsTests.post
        # которому добавлен тэг, иначе страница вывода постов по тегу будет пустой
        post.tags.add(tag)
        expected_absolute_url = '/tag/' + tag.slug + '/'
        response = self.authorized_client.get(expected_absolute_url)
        self.assertTemplateUsed(response, 'blog/posts_by_tags.html')

    def test_search_uses_correct_template(self):
        """Search использует корректный шаблон
        Поиск создает маршрут вида '/search/?q=test+title', а название поста выглядит как Test Title.
        Поэтому передавать в value url следует именной такой машрут.
        """
        post = BlogURLsTests.post
        title = post.title.lower().replace(' ', '+')
        url = '{url}?{filter}={value}'.format(
            url='/search/',
            filter='q',
            value=title
        )
        User.objects.create_user(username='IvanovIvan1', password='123456', first_name='Ivan', last_name='Ivanov',
                                 email='ivanov@gmail.com')
        self.authorized_client.login(username='IvanovIvan1', password='123456')
        response = self.authorized_client.get(url)
        self.assertTemplateUsed(response, 'blog/homepage.html')
