# Форма, связанная с моделью
from django.forms import ModelForm

from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags', 'preview_image', 'images', ]
        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'content': forms.Textarea(attrs={'cols': 79, 'rows': 20}),
            'tags': forms.Select(),
        }
