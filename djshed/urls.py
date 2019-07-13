from django.urls import path, re_path
from django.conf.urls import url

from djshed import views

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    re_path(
        r'^(?P<program>[-\w]+)/(?P<term>[-\w]+)/(?P<year>\d+)/(?P<content_type>[-\w]+)/',
        views.schedule, name='schedule'
    ),
    re_path(
        r'^(?P<program>[-\w]+)/(?P<term>[-\w]+)/(?P<year>\d+)/',
        views.schedule, name='schedule'
    ),
    path('', views.home, name='home'),
]
