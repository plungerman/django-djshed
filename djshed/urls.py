# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy
from djauth.views import loggedout
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from djshed import views


handler404 = 'djtools.views.errors.four_oh_four_error'
handler500 = 'djtools.views.errors.server_error'


urlpatterns = [
    # auth
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(),
        {'template_name': 'registration/login.html'},
        name='auth_login',
    ),
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),
        {'next_page': reverse_lazy('auth_loggedout')},
        name='auth_logout',
    ),
    path(
        'accounts/loggedout/',
        loggedout,
        {'template_name': 'registration/logged_out.html'},
        name='auth_loggedout',
    ),
    path(
        'accounts/',
        RedirectView.as_view(url=reverse_lazy('auth_login')),
    ),
    path(
        'denied/',
        TemplateView.as_view(template_name='denied.html'),
        name='access_denied',
    ),
    # django admin
    path('rocinante/', admin.site.urls),
    path(
        '<str:program>/<str:term>/<str:year>/',
        views.schedule,
        name='schedule',
    ),
    path(
        '<str:program>/<str:term>/<str:year>/',
        views.schedule,
        name='schedule',
    ),
    path('', views.home, name='home'),
]
