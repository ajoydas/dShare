from django.conf.urls import url
from django.views import generic

from insurance import views

app_name = 'insurance'

urlpatterns = [
    url(r'^$', views.profile, name='profile'),
    url(r'view_record$', views.view_record, name='view_record'),
]
