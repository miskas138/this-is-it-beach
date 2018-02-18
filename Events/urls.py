from django.conf.urls import url
from . import views
from django.conf.urls import include

urlpatterns = [
#post create
    url(r'^event_create/$', views.event_create, name='event_create'),
    url(r'^home/$', views.home_page, name='home_page'),
    url(r'^event_details/(?P<pk>[0-9]+)/$', views.event_details, name='event_details'),
    url(r'^organizers/$', views.user_list, name='user_list'),
    url(r'^event_like/$', views.event_like, name='like'),
    # register to post
    url(r'^event/register/$', views.event_register, name='event_register'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.home_page, name='home_page_by_tag'),
    url(r'^tinymce/', include('tinymce.urls')),
]