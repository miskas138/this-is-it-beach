from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.admin import AdminSite

class Profile_Admin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'photo', 'gender')

class Advanced_Profile_Admin(admin.ModelAdmin):
    list_display = ('user', 'organization_name')


admin.site.register(Profile, Profile_Admin)
admin.site.register(Advanced_Profile, Advanced_Profile_Admin)