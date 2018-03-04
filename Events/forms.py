from django.contrib.auth.models import User
from taggit.forms import TagField, TagWidget
from tinymce.widgets import TinyMCE

from .models import *
from django import forms
from datetimewidget.widgets import DateTimeWidget

class EventCreateForm(forms.ModelForm):
    title = forms.CharField(label='Τίτλος')
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
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