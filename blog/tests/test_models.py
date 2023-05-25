""" Тесты для моделей приложения blog
!WARNING!
Для работы с тестами необходимо ознакомится с документацией 'Тестирование' в разделе WasHere/settings.py
"""
from django.test import TestCase
from blog.models import Profile, Tag, Post, transform_tags_str_to_list, create_tags_from_list
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist


class ProfileModelTests(TestCase):
    """ Тесты для модели Profile"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """ Создаем тестовую запись в БД
        сохраняем созданную запись в качестве переменной класса"""
        # Тестовая запись User
        cls.user = User.objects.create(username='IvanovIvan', first_name='Ivan', last_name='Ivanov',
                                   email='ivanov@gmail.com')

    def test_signal_create_profile(self):
        """ При создании User по сигналу происходит создание Profile с Profile.user=User
        (связь один к одному). Если после создания User в модели Profile появилась такая запись -
        сигнал работает правильно"""
        user = ProfileModelTests.user
        try:
            profile = Profile.objects.get(user=user)
            print('test passed!')
        except ObjectDoesNotExist:
            print('test failed! User doesnt created in Profile model')

    def test_failed_duplicated_users(self):
        """ Проверка на добавление уже существующего пользователя"""
        user = ProfileModelTests.user
        # пытаемся создать точно такого же пользв.
        try:
            User.objects.create(username='IvanovIvan', first_name='Ivan',
                                                            last_name='Ivanov', email='user@gmail.com')
        except IntegrityError:
            print('Test passed! Can not duplicate user!')

    def test_profile_name_is_user_username(self):
        """ __str__ Profile это строка с содержимым user.username"""
        user = ProfileModelTests.user
        profile = Profile.objects.get(user=user)
        expected_profile_name = user.username
        self.assertEqual(expected_profile_name, str(profile))

    def test_profile_about(self):
        """ Описание профиля about_user соответствует задаваемому пользователем"""
        user = ProfileModelTests.user
        profile = Profile.objects.get(user=user)
        about_msg = 'Информация о пользователе'
        # добавим описание к профилю
        profile.about_user = about_msg
        self.assertEqual(profile.about_user, about_msg)

    def test_profile_verbose_name(self):
        """ Полученное из Meta модели Profile verbose_name"""
        user = ProfileModelTests.user
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile._meta.verbose_name.title(), 'Профиль')

    def test_profile_verbose_name_plural(self):
        """ Полученное из Meta модели Profile verbose_name_plural"""
        user = ProfileModelTests.user
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile._meta.verbose_name_plural.title(), 'Профили')


class TagModelTests(TestCase):
    """ Тесты для модели Tag"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """ Создаем тестовую запись в БД
        сохраняем созданную запись в качестве переменной класса"""
        cls.tag = Tag.objects.create(title='Тест', slug='test')

    def test_tag_representation(self):
        """ __str__ возвращает название тэга"""
        tag = TagModelTests.tag
        self.assertEqual(tag.title, str(tag))

    def test_get_absolute_url(self):
        """ get_absolute_url возвращает нужный слаг
        с точки зрения модели """
        tag = TagModelTests.tag
        expected_absolute_url = '/tag/' + tag.slug + '/'
        self.assertEqual(expected_absolute_url, tag.get_absolute_url())

    def test_tag_verbose_name(self):
        """ Полученное из Meta модели Tag verbose_name"""
        tag = TagModelTests.tag
        self.assertEqual(tag._meta.verbose_name.title(), 'Тэг')

    def test_tag_verbose_name_plural(self):
        """ Полученное из Meta модели Tag verbose_name_plural"""
        tag = TagModelTests.tag
        self.assertEqual(tag._meta.verbose_name_plural.title(), 'Тэги')

    def test_transfrom_tags_str_to_list(self):
        """ Функция преобразует строку с тэгами в список"""
        tags_string = 'mew mew, новый тест, проверка'
        tags_list = transform_tags_str_to_list(tags_string)
        self.assertEqual(isinstance(tags_list, list), True)

    def test_create_tags_from_list(self):
        """ Функция преобразует список тэгов в словарь тэгов"""
        tags_list = ['mew mew, новый тест, проверка']
        tags_dict = create_tags_from_list(tags_list)
        self.assertEqual(isinstance(tags_dict, dict), True)

    def test_create_tags_from_list_uses_correct_logic(self):
        """ Функция реобразования списка тэгов в словарь вида тэг:слаг_тэга
        слаг_тэга получается переводом названия тэга на латиницу и вызовом slugify"""
        # исходный список тэгов
        tags_list = ['Категория', 'Test cat', 'Новая категория']
        excpected_tags_dict = {'Категория': 'kategorija', 'Test cat': 'test-cat', 'Новая категория': 'novaja-kategorija'}
        # полученный словарь из исходного списка тэгов
        tags_dict = create_tags_from_list(tags_list)
        self.assertEqual(excpected_tags_dict, tags_dict)


class PostModelTests(TestCase):
    """ Тесты для модели Post"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        """ Создаем тестовую запись в БД
        сохраняем созданную запись в качестве переменной класса
        Примечание: поскольку в модели используется автор как внешний ключ к User, и поле тэгов со связью многие со многими,
        для тестирования функционирования поста необходимо создать и автора и тэг"""
        cls.tag = Tag.objects.create(title='Тест', slug='test')
        cls.user = User.objects.create(username='IvanovIvan', first_name='Ivan', last_name='Ivanov',
                                       email='ivanov@gmail.com')
        cls.post = Post.objects.create(title='Test Title', author=cls.user, content='Test post content', slug='test-title')
        cls.post.tags.add(cls.tag)

    def test_save_create_post_slug(self):
        """ слаг поста, определяемый методом save(), добавляется при создании поста
        в соответствии с правилами создания слага"""
        post = PostModelTests.post
        expected_post_slug = 'test-title'
        self.assertEqual(expected_post_slug, post.slug)

    def test_get_absolute_url(self):
        """ get_absolute_url возвращает нужный слаг
        с точки зрения модели """
        post = PostModelTests.post
        expected_absolute_url = '/post/' + post.slug + '/'
        self.assertEqual(expected_absolute_url, post.get_absolute_url())

    def test_post_slug_len(self):
        """ слаг поста ограничен 100 первыми символами названия"""
        # создадим новый пост, название которого будет больше 100 символов
        user = PostModelTests.user
        very_long_string = 20*'string'
        post = Post.objects.create(title=very_long_string, author=user, content='Test post content')
        self.assertEqual(100, len(post.slug))

    def test_post_representation(self):
        """__str__ возвращает название поста"""
        post = PostModelTests.post
        self.assertEqual(post.title, str(post))

    def test_unique_title_content_constraints(self):
        """ Запрет создания поста с существующими в БД title и content"""
        post = PostModelTests.post
        # создание нового тэга
        user = User.objects.create(username='PetrovPent', first_name='Petr', last_name='Petrov',
                                       email='petrov@gmail.com')
        # создание полностью идентичного поста как в setUp
        # тэг на данном этапе не критичен
        try:
            post = Post.objects.create(title='Test Title', author=user, content='Test post content')
        except IntegrityError:
            print('Test passed! Can not duplicate post!')
