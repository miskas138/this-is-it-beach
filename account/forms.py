from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from datetimewidget.widgets import DateWidget, DateTimeWidget

from .models import *

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Κωδικός Πρόσβασης', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Επαλήθευση κωδικού πρόσβασης', widget=forms.PasswordInput)
    username = forms.CharField(label='Όνομα χρήστη')
    first_name = forms.CharField(label='Όνομα')
    last_name = forms.CharField(label='Επίθετο')
    email = forms.EmailField(label='Ηλεκτρονικό ταχυδρομείο', widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont\'t match you fucking idiot')
        return cd['password2']

YEARS= [x for x in range(1950, timezone.now().year+1)]
MONTHS = {1:'Ιανουάριος', 2:'Φεβρουάριος', 3:'Μάρτιος', 4:'Απρίλιος', 5:'Μάιος', 6:'Ιούνιος', 7:'Ιούλιος', 8:'Αύγουστος', 9:'Σεπτέμβριος',
          10:'Οκτώβριος', 11:'Νοέμβριος', 12:'Δεκέμβριος'}
class ProfileEditForm(forms.ModelForm):
    gender = forms.ChoiceField(label='Φύλο', choices=USER_GENDER_CHOISES, widget=forms.Select(attrs={'class':'form-control'}))
    photo = forms.ImageField(label='Εικόνα προφίλ', widget=forms.FileInput)
    date_of_birth = forms.DateField(label='Ημερομηνία γέννησης', widget=DateWidget(attrs={'class': 'form-control'}, usel10n=True, bootstrap_version=3))

    class Meta:
        model = Profile
        fields = ('gender', 'photo', 'date_of_birth')

class AdvancedProfileEditForm(forms.ModelForm):
    organization_name = forms.CharField(label='Ονομασία οργανισμού')
    description = forms.Textarea()
    address = forms.CharField(label='Διεύθυνση')
    city = forms.CharField(label='Πόλη')
    phone_number = forms.IntegerField(label='Τηλέφωνο')
    photo = forms.ImageField(label='Εικόνα προφίλ', widget=forms.FileInput)

    class Meta:
        model = Advanced_Profile
        exclude = ('user_type', 'user')


class UserEditForm(forms.ModelForm):
    username = forms.CharField(label='Όνομα χρήστη')
    first_name = forms.CharField(label='Όνομα')
    last_name = forms.CharField(label='Επίθετο')
    email = forms.EmailField(label='Ηλεκτρονικό ταχυδρομείο', widget=forms.EmailInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


