# -*- coding: utf-8 -*-

from django.urls import path
from djshed import views


handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    path(
        '<str:program>/<str:term>/<str:year>/<str:content_type>/',
        views.schedule, name='schedule',
    ),
    path(
        '<str:program>/<str:term>/<str:year>/',
        views.schedule, name='schedule',
    ),
    path('', views.home, name='home'),
]
