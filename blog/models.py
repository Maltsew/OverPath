from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


# Модель профиля пользователя
class Profile(models.Model):
    name = models.CharField(max_length=20, verbose_name='Имя пользователя')
    username = models.CharField(max_length=20, verbose_name='Ник пользователя')
    user_email = models.EmailField(verbose_name='эл. адрес пользователя')
    about_user = models.TextField(verbose_name='Короткое описание профиля')
    profile_image = models.FileField(upload_to='profile_uploads/profile_pics/')

    def __str__(self):
        return f'{self.username} {self.user_email}'

    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'


# Модель категории - класс, объединяющий посты по схожему признаку
class Category(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название категории', db_index=True)
    subtitle = models.CharField(max_length=20, verbose_name='Подзаголовок категории', null=True, blank=True)
    thumbnail = models.FileField(upload_to='category_uploads/cats/')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

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
    # для поста 1 картинка - как превью, для отображения на домашней странице
    preview_image = models.FileField(upload_to='category_uploads/post_preview_upload/', verbose_name='Картинка для превью')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')


    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        # Совместная комбинация названия и содержания поста должны быть уникальными в пределах таблицы в БД
        # (защита от дублирования постов)
        constraints = (
            models.UniqueConstraint(fields=('title', 'content'),
                                    name='%(app_label)s_%(class)s_title_content_constraint'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    image = models.FileField(upload_to='category_uploads/post_content_upload/', verbose_name='Image')


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)
