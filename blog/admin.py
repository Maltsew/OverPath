from django.contrib import admin
from blog.models import Profile, Post, Tag


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_email')
    # Последовательность имен полей, которые будут преобразованы в гиперссылки на страницы правки записи
    list_display_links = ('username',)
    search_fields = ('user', 'username', 'user_email')


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    search_fields = ('title', )
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on',)
    list_display_links = ('title',)
    search_fields = ('title', 'author', 'created_on')
    prepopulated_fields = {'slug': ('title', 'author')}


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
