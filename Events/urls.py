from django.conf.urls import url
from . import views

urlpatterns = [
#post create
    url(r'^event_create/$', views.event_create, name='event_create'),
    url(r'^home/$', views.home_page, name='home_page'),
    url(r'^event_details/(?P<pk>[0-9]+)/$', views.event_details, name='event_details'),
    url(r'^organizers/$', views.user_list, name='user_list'),
    url(r'^event_like/$', views.event_like, name='like'),
]