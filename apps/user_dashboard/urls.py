from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^users/new$', views.new, name='new'),
    url(r'^users/show/(?P<id>\d+)$', views.show, name='show'),
    url(r'^users/edit/(?P<id>\d+)$', views.edit, name='edit'),
    url(r'^post_message/(?P<id>\d+)$', views.post_message, name='post_message'),
    url(r'^post_comment/(?P<id>\d+)$', views.post_comment, name='post_comment')
]
