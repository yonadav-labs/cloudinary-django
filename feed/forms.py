from django.forms import ModelForm
from cloudinary.forms import CloudinaryJsFileField
from .models import Loop
from django import forms


class FeedForm(ModelForm):
    class Meta:
        model = Loop
        fields = ('image', 'text', 'link',)
        widgets = {
            'text': forms.TextInput(
                attrs={'id': 'post-text', 'required': True, 'placeholder': 'Add text', 'class': 'text'}
            ),
            'link': forms.TextInput(
                attrs={'id': 'post-link', 'placeholder': 'Add link', 'class': 'text link'}
            ),
        }
        labels = {
            'image': '',
            'text': '',
            'link': ''
        }


class FeedDirectForm(FeedForm):
    image = CloudinaryJsFileField()

