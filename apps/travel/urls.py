from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels/add$', views.add),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^travels$', views.travels),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination),
    url(r'^add$', views.inserting),
]
