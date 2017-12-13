from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Profile, USER_TYPE_CHOISES

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
            raise forms.ValidationError('Passwords dont\'t match')
        return cd['password2']

YEARS= [x for x in range(1950, timezone.now().year+1)]
class ProfileEditForm(forms.ModelForm):
    gender = forms.ChoiceField(label='Φύλο', choices=USER_TYPE_CHOISES)
    photo = forms.ImageField(label='Εικόνα προφίλ', widget=forms.FileInput)
    date_of_birth = forms.DateField(label='Ημερομηνία γέννησης', widget=forms.SelectDateWidget(years=YEARS))
    class Meta:
        model = Profile
        fields = ('gender', 'photo', 'date_of_birth')

