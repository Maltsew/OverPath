from django.contrib import admin
from blog.models import Profile, Post, Category


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    # Последовательность имен полей, которые будут преобразованы в гиперссылки на страницы правки записи
    list_display_links = ('user',)
    search_fields = ('user',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle')
    list_display_links = ('title',)
    search_fields = ('title', 'subtitle')


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'slug')
    list_display_links = ('title',)
    search_fields = ('title', 'author', 'created_on')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
