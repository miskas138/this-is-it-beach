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


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'body')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created')


class RegisterAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created')

class ViewAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created')

class VideoUploadAdmin(admin.ModelAdmin):
    list_display = ('event','user','created')

class Mp3UploadAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created')

class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'created')


admin.site.register(ImageUpload, ImageUploadAdmin)
admin.site.register(View, ViewAdmin)
admin.site.register(Register, RegisterAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Information, InformationAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(VideoUpload, VideoUploadAdmin)
admin.site.register(Mp3Upload, Mp3UploadAdmin)