# Форма, связанная с моделью
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django import forms
from .models import Post, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'tags', 'preview_image', 'images', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
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


class ProfileRegistrationForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
