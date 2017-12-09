from django.db import models
from django.db import models
from django.conf import settings
# Create your models here.



USER_TYPE_CHOISES = (('MALE', 'male'), ('FEMALE', 'female'))
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/%y/%m/%d', blank=True, null=True)
    gender = models.CharField(max_length=6, choices=USER_TYPE_CHOISES, default='MALE', blank=True)
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

