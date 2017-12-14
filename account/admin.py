from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.admin import AdminSite

class Profile_Admin(admin.ModelAdmin):
    list_display = ('date_of_birth', 'photo', 'gender')


admin.site.register(Profile, Profile_Admin)
