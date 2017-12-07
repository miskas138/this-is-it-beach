from django.conf.urls import url
from django.contrib.auth import views as DjangoViews
from . import views

urlpatterns = [
    # register urls
    url(r'^login/$', DjangoViews.login, name='login'),
    url(r'^logout/$', DjangoViews.logout, name='logout'),
    url(r'^$', views.dashboard, name='dashboard'),

]