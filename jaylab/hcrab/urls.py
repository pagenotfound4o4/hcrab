#coding=utf-8
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^dropbox/signin/$', views.dropbox_sign),
    url(r'^dropbox/authorize')
)

