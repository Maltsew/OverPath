from django.contrib import admin
from blog.models import Profile, Post, Tag
from django.contrib import auth
import django.contrib.auth.models


admin.site.unregister(auth.models.Group)


# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    pass


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


