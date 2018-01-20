from django.conf.urls import url
from . import views

urlpatterns = [
#post create
    url(r'^event_create/$', views.event_create, name='event_create'),
    url(r'^home/$', views.home_page, name='home_page'),
]