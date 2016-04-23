from django.conf.urls import url

from . import views
from django.views.generic import TemplateView
import allauth.account.views as aviews

urlpatterns = [
    url(r'^login/$', aviews.login),
    url(r'^callback/$', views.callback),
    url(r'^facebook/$', views.facebook_redirect),
    url(r'^cian/$', views.cian)
]
