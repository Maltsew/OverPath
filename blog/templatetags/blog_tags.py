from django import template
from blog.models import Tag, Post


register = template.Library()


@register.simple_tag()
def get_posts(filter=True):

    ''' если фильтр True (по дефолту), простой тэг возвращает queruset всех постов в шаблон homepage,
    иначе возвращает 3 последних поста (порядок задает модель)'''
    # проверка на наличие хоть одного поста
    if filter:
        return Post.objects.all()
    else:
        return Post.objects.all()[:3]


@register.simple_tag()
def get_all_tags():
    return Tag.objects.all()


@register.simple_tag()
def get_tags_count():
    return Tag.objects.all().count()
