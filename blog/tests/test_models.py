from django.test import TestCase
from django.urls import reverse

from blog.models import Profile, Tag
from django.contrib.auth.models import User

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from unittest import skip

from blog.views import BlogTags


""" Тесты для моделей приложения blog
!WARNING!
Для работы с тестами необходимо ознакомится с документацией 'Тестирование' в разделе WasHere/settings.py
"""


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

    def test_tag_represent(self):
        """ __str__ возвращает название тэга"""
        tag = TagModelTests.tag
        self.assertEqual(tag.title, str(tag))

    def test_get_absolute_url(self):
        """ get_absolute_url возвращает нужный слаг
        с точки зрения модели """
        tag = TagModelTests.tag
        expected_absolute_url = '/blog/tag/' + tag.slug + '/'
        self.assertEqual(expected_absolute_url, tag.get_absolute_url())

    def test_tag_verbose_name(self):
        """ Полученное из Meta модели Tag verbose_name"""
        tag = TagModelTests.tag
        self.assertEqual(tag._meta.verbose_name.title(), 'Тэг')

    def test_tag_verbose_name_plural(self):
        """ Полученное из Meta модели Tag verbose_name_plural"""
        tag = TagModelTests.tag
        self.assertEqual(tag._meta.verbose_name_plural.title(), 'Тэги')
