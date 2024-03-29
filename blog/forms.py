from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django import forms
from .models import Post, Profile, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from blog.views import transform_tags_str_to_list


class PostForm(forms.ModelForm):
    """ Форма создания нового поста
    model: Post
    fields: title, content, preview_image, images, slug
    widgets:
        title: forms.TextInput
        content: forms.Textarea
    tags: Тэги добавляются к посту как get_or_create тэгов из модели Tag. Тэгов может быть введено несколько,
    в таком случае они разделяются запятой и поочередно добавляются к посту
    """
    tags = forms.CharField(label='Категории', max_length=200,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'Если категорий несколько, укажите их через запятую',
                                     'size': 79}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'preview_image', 'images']
        widgets = {
            'title': forms.TextInput(attrs={'size': 79}),
            'content': forms.Textarea(attrs={'cols': 79, 'rows': 20}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data['title']
        content = cleaned_data['content']
        p1 = Post.objects.filter(title=title).exists()
        p2 = Post.objects.filter(content=content).exists()

        if p1 and p2:
            msg = 'Такой пост уже существует'
            self.add_error('title', msg)
            raise forms.ValidationError(msg, code='invalid')
        return cleaned_data

    def clean_tags(self):
        cleaned_data = self.cleaned_data
        tags = cleaned_data['tags']
        tags = transform_tags_str_to_list(tags)
        # TODO валидация поля (отбросить все пробелы и просмотр только чсимволов)
        for tag in tags:
            if tag in (',', ', ', '', ' ',):
                msg = 'Укажите категорию'
                raise forms.ValidationError(msg, code='invalid')
        return tags


class ProfileLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ProfileRegistrationForm(UserCreationForm):
    about_user = forms.CharField(label='Расскажите о себе', max_length=200,
                                 widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    profile_image = forms.FileField(label='Добавьте аватар')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'size': 60}),
            'last_name': forms.TextInput(attrs={'size': 60}),
            'username': forms.TextInput(attrs={'size': 60}),
            'email': forms.TextInput(attrs={'size': 60}),
            'password1': forms.PasswordInput(),
            'password1': forms.PasswordInput(),
        }

    def clean_about_user(self):
        about_user = self.cleaned_data['about_user']
        return about_user

    def clean_profile_image(self):
        profile_image = self.cleaned_data['profile_image']
        return profile_image

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data
