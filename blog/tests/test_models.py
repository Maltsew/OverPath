from django.test import TestCase
from blog.models import Profile
from django.contrib.auth.models import User

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from unittest import skip


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
