from django.db import models
from django.conf import settings
from django.urls import reverse
from geoposition.fields import GeopositionField
from taggit.managers import TaggableManager
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from account.models import Advanced_Profile


SECTION_CHOISES = (('ΜΟΥΣΙΚΗ', 'Μουσική'),
                   ('ΘΕΑΤΡΟ', 'Θέατρο'),
                   ('ΧΟΡΟΣ', 'Χορός'),
                   ('ΕΚΘΕΣΗ', 'Έκθεση'),
                   ('ΚΙΝΗΜΑΤΟΓΡΑΦΟΣ', 'Κινηματογράφος'),
                   ('ΔΙΑΦΟΡΕΣ', 'Διάφορες'))


class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='events_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    section = models.CharField(max_length=20, choices=SECTION_CHOISES, default='ΜΟΥΣΙΚΗ')
    tags = TaggableManager()
    content = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_details', args=[self.pk])

class Information(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(blank=True, null=True)
    ticket_price = models.FloatField()
    presale = models.CharField(max_length=200, blank=True, null=True)

class Location(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='location')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    tel = models.IntegerField()
    city = models.CharField(max_length=20)
    site = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    position = GeopositionField()

class Comment(models.Model):
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user.username, self.event)


class UserComment(models.Model):
    profile = models.ForeignKey(Advanced_Profile, related_name='user_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile_comments', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user.username, self.profile)


class Like(models.Model):
    event = models.ForeignKey(Event, related_name='likes', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes', blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.title

class Register(models.Model):
    event = models.ForeignKey(Event, related_name='register', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='register', blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.event.title

class View(models.Model):
    event = models.ForeignKey(Event, related_name='view', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='viewed', blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return self.event.title



class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


#add a field in user model dynamically
User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers',
                                                      symmetrical=False))


class VideoUpload(models.Model):
    event = models.ForeignKey(Event, related_name='video_uploads', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='video_uploads', blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='event_video_uploads/%D/%M/%Y', blank=True, null=True)
    class Meta:
        ordering = ('-created',)