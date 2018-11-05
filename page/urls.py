from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^traceroute', views.traceroute, name="traceroute"),
    url(r'^ping', views.ping, name='ping'),
]