from django.contrib.auth.models import User
from .models import *
from  django import forms


class PostCreateForm(forms.ModelForm):
    def clean_file(self):
        file = self.cleaned_data['file']
        if (file.name.endswith('mp4') or file.name.endswith('MP4')):
            return file
        else:
            raise forms.ValidationError('The given file does not match valid video extensions.')
    class Meta:
        model = Post
        exclude = ('author', 'users_like',)