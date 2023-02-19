from django.db import models
from django.urls import reverse


# Модель профиля пользователя
class Profile(models.Model):
    name = models.CharField(max_length=20, verbose_name='Имя пользователя')
    username = models.CharField(max_length=20, verbose_name='Ник пользователя')
    user_email = models.EmailField(verbose_name='эл. адрес пользователя')
    about_user = models.TextField(verbose_name='Короткое описание профиля')
    # profile_image = models.ImageField(default='default.jpeg', upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return f'{self.username} {self.user_email}'

    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'


# Модель категории - класс, объединяющий посты по схожему признаку
class Category(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название категории', db_index=True)
    subtitle = models.CharField(max_length=20, verbose_name='Подзаголовок категории', null=True, blank=True)
    #thumbnail = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


# Модель "пост" - основной тип публикуемой информации в блоге
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название поста')
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name='Автор')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Дата обновления поста')
    content = models.TextField(verbose_name='Содержание поста')
    # categories = models.ManyToManyField(Category)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    #image = models.ImageField(null=True, blank=True, upload_to='images/')

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        # Совместная комбинация названия и содержания поста должны быть уникальными в пределах таблицы в БД
        # (защита от дублирования постов)
        constraints = (
            models.UniqueConstraint(fields=('title', 'content'), name='%(app_label)s_%(class)s_title_content_constraint'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_post', kwargs={'post_id': self.pk})
