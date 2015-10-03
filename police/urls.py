from django.conf.urls import patterns, url
from police import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^index$', views.index, name='index'),
        url(r'^deploy$', views.deploy, name='deploy'),
]
