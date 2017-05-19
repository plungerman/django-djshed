from django.conf.urls import include, url
from django.views.generic import TemplateView

from djshed import views

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = [
    url(
        r'^(?P<program>[-\w]+)/(?P<term>[-\w]+)/(?P<year>\d+)/$',
        views.schedule, name='schedule'
    ),
    url(
        r'^$',
        views.home, name='home'
    ),
]
