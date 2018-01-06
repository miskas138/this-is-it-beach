from django.contrib.auth.models import User
from .models import *
from django import forms
from datetimewidget.widgets import DateTimeWidget

class EventCreateForm(forms.ModelForm):
    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            if (image.name.endswith('jpg') or image.name.endswith('JPG')):
                return image
            else:
                raise forms.ValidationError('Η μορφή του αρχείου της εικονας πρέπει να είναι jpg')

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
