from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from taggit.forms import TagField, TagWidget
from tinymce.widgets import TinyMCE

from .models import *
from django import forms
from datetimewidget.widgets import DateTimeWidget

class EventCreateForm(forms.ModelForm):
    title = forms.CharField(label='Τίτλος')
    content = forms.CharField(widget=TinyMCE())
    tags = TagField(label='Ετικέτες', help_text='δημιούργησε tag για την εκδήλωση διαχωρίζοντας με κόμματα, ή επέλεξε από την παρακάτω λίστα',
                    widget=TagWidget(attrs={'class': 'form-control tagman'}))
    section = forms.ChoiceField(label='Κατηγορία', choices=SECTION_CHOISES, widget=forms.Select(attrs={'class':'form-control'}))

    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            if (image.name.endswith('jpg') or image.name.endswith('JPG') or image.name.endswith('png') or image.name.endswith('PNG')):
                return image
            else:
                raise forms.ValidationError('Η μορφή του αρχείου της εικονας πρέπει να είναι jpg ή png')

    class Meta:
        model = Event
        exclude = ('user',)

class LocationForm(forms.ModelForm):

    class Meta:
        model = Location
        exclude = ('event',)

class InformationForm(forms.ModelForm):
    dateTime = forms.DateTimeField(label='Ημερομηνία και ώρα εκδήλωσης',
                                   widget=DateTimeWidget(attrs={'class': 'form-control'}, usel10n=True,
                                                         bootstrap_version=3))
    ticket_price = forms.IntegerField(label='Τιμή εισητηρίου')
    presale = forms.CharField(label='Προπώληση')
    class Meta:
        model = Information
        exclude = ('event',)



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'cols': 25, 'class': 'form-control'}),
        }


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5, 'cols': 25, 'class': 'form-control'}),
        }

class VideoUploadForm(forms.ModelForm):
    def clean_video(self):
        video = self.cleaned_data['video']
        if video:
            if (video.name.endswith('mp4') or video.name.endswith('MP4')):
                return video
            else:
                raise forms.ValidationError('Το format του video πρέπει να είναι MP4')
        else:
            raise forms.ValidationError('Δεν επιλέξατε αρχείο')

    class Meta:
        model = VideoUpload
        exclude = ('user', 'event')


class Mp3UploadForm(forms.ModelForm):
    def clean_mp3(self):
        mp3 = self.cleaned_data['mp3']
        if mp3:
            if (mp3.name.endswith('mp3') or mp3.name.endswith('MP3')):
                return mp3
            else:
                raise forms.ValidationError('Το μουσικό αρχείο που επιλέξατε δεν είναι mp3')
        else:
            raise forms.ValidationError('Δεν έχετε επιλέξει mp3')

    class Meta:
        model = Mp3Upload
        exclude = ('user', 'event')


class ImageUploadForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            if (image.name.endswith('jpg') or image.name.endswith('JPG') or image.name.endswith('png') or image.name.endswith('PNG')):
                return image
            else:
                raise forms.ValidationError('The given file does not match valid jpg or png extension.')
        else:
            raise forms.ValidationError('You havent selected any image!!!')

    class Meta:
        model = ImageUpload
        exclude = ('user', 'event')