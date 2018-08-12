from django.conf.urls import url
from django.views import generic

from user import views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'view_receiver/(?P<pk>[0-9]+)$', views.view_receiver, name='view_receiver'),
    url(r'add_receiver/(?P<pk>[0-9]+)$', views.add_receiver, name='add_receiver'),
    url(r'add_policy$', views.add_policy, name='add_policy'),
    url(r'add_record_policy/(?P<pk>[0-9]+)', views.add_record_policy, name='add_record_policy'),
url(r'add_record$', views.add_record, name='add_record'),
    url(r'view_record/(?P<pk>[0-9]+)$', views.view_record, name='view_record'),
]
