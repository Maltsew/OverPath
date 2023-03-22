# Форма, связанная с моделью
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django import forms
from .models import Post, Profile, Tag
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'preview_image', 'images', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'content': forms.Textarea(attrs={'cols': 79, 'rows': 20}),
            'tags': forms.SelectMultiple(attrs={'size': 10, 'class': 'chosen'}),
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
