from django import template
from blog.models import Tag, Post
from django.db.models import Max


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


@register.simple_tag()
def get_tag_uses_counter():
    t = Tag.objects.all()
    # если тэгов пока нет, вернет пустой словарь для обработки исключения,
    # тогда в популярных тэгах следует выводить сообщение
    if len(t) == 0:
        return {}
    tags_dict = {}
    # для каждого тэга найдем количество раз, когда он используется
    for tag in t:
        counter = tag.post_set.all().count()
        tags_dict[tag] = counter
    # отсортируем в словаре 3 самых популярных поста
    tag_counter = sorted(tags_dict.items(), key=lambda item: item[1], reverse=True)
    # возвращает пары тэг:количество_использований
    return dict(tag_counter[:3])
