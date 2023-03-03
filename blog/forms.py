# Форма, связанная с моделью
from django.forms import ModelForm

from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'tags', 'preview_image', 'images', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'size': 80}),
            'content': forms.Textarea(attrs={'cols': 79, 'rows': 20}),
        }

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data['title']
        content = cleaned_data['content']
        if title and Post.objects.get(title=title):
            if content and Post.objects.get(content=content):
                msg = 'Такой пост уже существует'
                self.add_error('title', msg)
                raise forms.ValidationError(("Такой пост уже существует"), code='invalid')
        return cleaned_data
