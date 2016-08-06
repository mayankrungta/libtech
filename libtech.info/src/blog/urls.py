from django.conf.urls import url

from .views import (
    blog_list,
    blog_create,
    blog_detail,
    blog_update,
    blog_delete,
)


urlpatterns = [
    url(r'^$', blog_list, name='list'),
    url(r'^create/$', blog_create),
    url(r'^(?P<id>\d+)/$', blog_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', blog_update),
    url(r'^(?P<id>\d+)/delete/$', blog_delete),
]
