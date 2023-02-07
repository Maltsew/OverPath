from django.db import models
from django.contrib.auth.models import User


''' В качестве модели пользователя используется models.User'''


# Модель профиля пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Профиль пользователя')
    # profile_image = models.ImageField(default='default.jpeg', upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'


# Модель категории - класс, объединяющий посты по схожему признаку
class Category(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название категории')
    subtitle = models.CharField(max_length=20, verbose_name='Подзаголовок категории', null=True, blank=True)
    slug = models.SlugField()
    #thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


# Модель "пост" - основной тип публикуемой информации в блоге
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название поста')
    slug = models.SlugField(max_length=200, unique=True, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Дата обновления поста')
    content = models.TextField(verbose_name='Содержание поста')
    categories = models.ManyToManyField(Category)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    #image = models.ImageField(null=True, blank=True, upload_to='images/')

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self):
        return self.title