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
    url(r'^home/(?P<section>[-\w]+)/$', views.home_page, name='home_page_section'),
    # user follow
    url(r'^users/follow/$', views.user_follow, name='user_follow'),

    url(r'^users/(?P<username>[-\w]+)/$', views.user_details, name='user_details'),
    # video uploads
    url(r'^event_details/(?P<pk>[0-9]+)/video_uploads/$', views.event_video_uploads, name='event_video_uploads'),
    # mp3 uploads
    url(r'^event_details/(?P<pk>[0-9]+)/mp3_uploads/$', views.event_mp3_uploads, name='event_mp3_uploads'),
    # image uploads
    url(r'^event_details/(?P<pk>[0-9]+)/image_uploads/$', views.event_image_uploads, name='event_image_uploads'),
]