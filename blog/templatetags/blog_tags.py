from django import template
from blog.models import Category, Post


register = template.Library()


@register.simple_tag()
def get_posts(filter=True):

    ''' если фильтр True (по дефолту), простой тэг возвращает queruset всех постов в шаблон homepage,
    иначе возвращает 3 последних поста (порядок задает модель)'''

    if filter:
        return Post.objects.all()
    else:
        return Post.objects.all()[:3]


@register.simple_tag()
def get_all_categories():
    return Category.objects.all()
