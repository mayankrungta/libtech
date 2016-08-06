from django.conf.urls import url

#Rest Framework
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    create_view,
    update_view,
    detail_view,
    detail_slug_view,
    list_view,
    WorkdetailCreateView,
    WorkdetailDetailView,
    WorkdetailDownloadView,
    WorkdetailListView,
    WorkdetailUpdateView,

    SerializerList,
    SerializerDetail,
    SerializerDetailSlug,
)

urlpatterns = [
    url(r'^$', WorkdetailListView.as_view(), name='list'),
    url(r'^create/$', create_view, name='create_view'),
    url(r'^add/$', WorkdetailCreateView.as_view(), name='create'),

    url(r'^api/$', SerializerList.as_view(), name='seriliazer_list'),
    url(r'^(?P<pk>\d+)/api$', SerializerDetail.as_view(), name='serializer_detail'),
    url(r'^(?P<slug>[\w-]+)/api$', SerializerDetailSlug.as_view(), name='serializer_detail_slug'),    
    
    url(r'^(?P<pk>\d+)/$', WorkdetailDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', WorkdetailDetailView.as_view(), name='detail_slug'),
    url(r'^(?P<pk>\d+)/download/$', WorkdetailDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/$', WorkdetailDownloadView.as_view(), name='download_slug'),
    url(r'^(?P<pk>\d+)/edit/$', WorkdetailUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/edit/$', WorkdetailUpdateView.as_view(), name='update_slug'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
