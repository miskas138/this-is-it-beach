from django.contrib import admin
from .models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'created']
    list_filter = ['created']

class InformationAdmin(admin.ModelAdmin):
    list_display = ['event', 'dateTime', 'ticket_price']
    list_filter = ['event', 'dateTime']

class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    list_filter = ['name']

admin.site.register(Event, EventAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Location, LocationAdmin)