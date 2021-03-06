"""libtech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

import contact.views
import blog
import profiles.views

urlpatterns = [
    url(r'^$', profiles.views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profile/', profiles.views.profile, name='profile'),
    url(r'^about/', profiles.views.about, name='about'),
    url(r'^contact/', contact.views.contact, name='contact'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^broadcasts/', include('broadcasts.urls', namespace='broadcasts')),
    url(r'^workdetails/', include('workdetails.urls', namespace='workdetails')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
