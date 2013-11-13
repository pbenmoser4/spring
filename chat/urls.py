from django.conf.urls import patterns, url

from chat import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
    url(r'^chat/', views.chat, name='chat'),
    url(r'^query/', views.query, name='query'),
)