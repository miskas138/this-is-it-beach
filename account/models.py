from django.db import models
from django.db import models
from django.conf import settings
from geoposition.fields import GeopositionField

# Create your models here.


USER_TYPE_CHOISES = (('SIMPLE_USER','simple_user'), ('ADVANCED_USER','advanced_user'))
USER_GENDER_CHOISES = (('MALE', 'Άνδρας'), ('FEMALE', 'Γυναίκα'))
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/%y/%m/%d', blank=True, null=True)
    gender = models.CharField(max_length=6, choices=USER_GENDER_CHOISES, default='MALE', blank=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOISES, default='SIMPLE_USER')
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class Advanced_Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='advanced_profile_photos', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOISES, default='ADVANCED_USER')
    position = GeopositionField(blank=True, null=True)
    def __str__(self):
        return 'Advanced Profile for user {}'.format(self.user.username)

