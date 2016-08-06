from django.conf.urls import url

#Rest Framework
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    BroadcastCreateView,
    BroadcastDetailView,
    BroadcastDownloadView,
    BroadcastListView,
    BroadcastUpdateView,

    SerializerList,
    SerializerDetail,
    SerializerDetailSlug,
)

urlpatterns = [
    url(r'^$', BroadcastListView.as_view(), name='list'),
    url(r'^add/$', BroadcastCreateView.as_view(), name='create'),

    url(r'^api/$', SerializerList.as_view(), name='seriliazer_list'),
    url(r'^(?P<pk>\d+)/api$', SerializerDetail.as_view(), name='serializer_detail'),
    url(r'^(?P<slug>[\w-]+)/api$', SerializerDetailSlug.as_view(), name='serializer_detail_slug'),    
    
    url(r'^(?P<pk>\d+)/$', BroadcastDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', BroadcastDetailView.as_view(), name='detail_slug'),
    url(r'^(?P<pk>\d+)/download/$', BroadcastDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/$', BroadcastDownloadView.as_view(), name='download_slug'),
    url(r'^(?P<pk>\d+)/edit/$', BroadcastUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/edit/$', BroadcastUpdateView.as_view(), name='update_slug'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
