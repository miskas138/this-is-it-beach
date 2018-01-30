from django.db import models
from django.conf import settings
from django.urls import reverse
from geoposition.fields import GeopositionField

SECTION_CHOISES = (('ΜΟΥΣΙΚΗ', 'Μουσική'), ('ΘΕΑΤΡΟ', 'Θέατρο'), ('ΧΟΡΟΣ', 'Χορός'), ('ΕΚΘΕΣΗ', 'Έκθεση'), ('ΚΙΝΗΜΑΤΟΓΡΑΦΟΣ',
                                                                                                      'Κινηματογράφος'))
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
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    tel = models.IntegerField()
    city = models.CharField(max_length=20)
    site = models.URLField(blank=True, null=True)
    position = GeopositionField()

