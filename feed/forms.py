from cloudinary.forms import CloudinaryJsFileField
from django import forms
from django.forms import ModelForm

from .models import Loop


class FeedForm(ModelForm):
    '''
    define the feed form with some customization
    '''

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

