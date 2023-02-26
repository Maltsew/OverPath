# Форма, связанная с моделью
from django.forms import ModelForm

from django import forms
from .models import Post, Images, Category


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content',]


class ImageForm(forms.ModelForm):
    image = forms.FileField(label='Image')

    class Meta:
        model = Images
        fields = ('image',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'subtitle',]
