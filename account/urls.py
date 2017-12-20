from django.conf.urls import url
from django.contrib.auth import views as DjangoViews
from . import views

urlpatterns = [
    # login/out urls
    url(r'^login/$', DjangoViews.login, name='login'),
    url(r'^logout/$', DjangoViews.logout, name='logout'),
    url(r'^$', views.dashboard, name='dashboard'),
    # change password
    url(r'^password-change/$', DjangoViews.password_change, name='password_change'),
    url(r'^password-change/done/$', DjangoViews.password_change_done, name='password_change_done'),

    # register
    url(r'^register/$', views.register_type, name='register_type'),
    url(r'^register/simple-user/$', views.register, name='register'),
    url(r'^register/advanced/$', views.advanced_register, name='advanced_register'),

    # reset password
    url(r'^password-reset/$', DjangoViews.password_reset, name='password_reset'),
    url(r'^password-reset/done/$', DjangoViews.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', DjangoViews.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password-reset/complete/$', DjangoViews.password_reset_complete, name='password_reset_complete'),

    # edit profile
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^edit/advanced/$', views.advanced_edit, name='advanced_edit'),

]