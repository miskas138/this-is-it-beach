from django.conf.urls import url
from . import views

urlpatterns = [
#post create
    url(r'^post_create/$', views.post_create, name='post_create'),
]