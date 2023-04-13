from django.test import TestCase
from blog.models import Profile


class ProfileTests(TestCase):
    """ Тесты для модели Profile"""

    @classmethod
    def setUpTestData(cls):
        """ Заносит данные в БД перед запуском тестов класса Profile"""
        cls.profile = Profile.objects.create(
            user='User',
            about_user='Test About User',
        )
