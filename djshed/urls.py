from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'

urlpatterns = patterns('djshed.views',
    url(
        r'^(?P<program>[-\w]+)/(?P<term>[-\w]+)/(?P<year>\d+)/$',
        'schedule', name="schedule"
    ),
    url(
        r'^$',
        'home', name="home"
    ),
)
