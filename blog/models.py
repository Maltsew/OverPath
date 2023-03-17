from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save




# Модель профиля пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    about_user = models.TextField(verbose_name='Короткое описание профиля')
    profile_image = models.FileField(upload_to='profile_uploads/profile_pics/')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name_plural = 'Профили'
        verbose_name = 'Профиль'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# Модель тэга - класс, объединяющий посты по схожему признаку
class Tag(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название категории', unique=True, db_index=True)
    thumbnail = models.FileField(upload_to='tags_uploads/post_tags/')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


    class Meta:
        verbose_name_plural = 'Тэги'
        verbose_name = 'Тэг'


# Модель "пост" - основной тип публикуемой информации в блоге
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название поста')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Автор')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Дата обновления поста')
    content = models.TextField(verbose_name='Содержание поста')
    tags = models.ManyToManyField(Tag)
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания поста')
    # Пока что, для превью фото выбирается отдельно
    preview_image = models.FileField(upload_to='post_uploads/post_images/', verbose_name='Превью поста')
    # А для наполнения поста
    images = models.FileField(upload_to='post_uploads/post_images/', verbose_name='Картинки поста', null=True, blank=True)
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
