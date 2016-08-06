import os

from mimetypes import guess_type

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
#from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper  # For 1.9 upwards

import django_tables2 as tables
from django_tables2 import RequestConfig, SingleTableView

from libtech.mixins import (
    LoginRequiredMixin,
    MultiSlugMixin,
    StaffRequiredMixin,
    SubmitButtonMixin,
)
from .models import Broadcast
from .form import BroadcastModelForm
from .mixins import BroadcastManagerMixin
from .serializers import BroadcastSerializer

#from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import generics
# Create your views here.

class BroadcastCreateView(LoginRequiredMixin, CreateView):
    model = Broadcast
    template_name = 'datetime_form.html'
    form_class = BroadcastModelForm
    # success_url = '/broadcasts/add/'
    submit_btn = 'Add Broadcast'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(BroadcastCreateView, self).form_valid(form)
        form.instance.managers.add(user)
        form.instance.user.mybroadcasts.broadcasts.add(form.instance) # FIXME Mynk
        # Add all default users form.instance.managers.add('admin')
        
        return valid_data

    '''
    def get_success_url(self):
        return reverse('broadcasts:list') # return '/users/%s/' % self.request.user
    '''
    
class BroadcastUpdateView(BroadcastManagerMixin, MultiSlugMixin, UpdateView):
    model = Broadcast
    template_name = 'form.html'
    form_class = BroadcastModelForm
    #success_url = '/broadcasts/'
    submit_btn = 'Update Broadcast'

class BroadcastDetailView(MultiSlugMixin, DetailView):
    model = Broadcast
    
class BroadcastDownloadView(MultiSlugMixin, DetailView):
    model = Broadcast

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj not in request.user.mybroadcasts.broadcasts.all():
            raise Http404
        filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
        wrapper = FileWrapper(open(filepath, 'rb'))

        mimetype = 'application/force-download'
        guessed_type = guess_type(filepath)[0]
        if guessed_type:
            mimetype = guessed_type
        response =  HttpResponse(wrapper, content_type=mimetype)   # HttpResponse('%s' % (obj))

        # Only for images and few other types preview would work so... 
        if not request.GET.get('preview'):
            response['Content-Disposition'] = 'attachment; filename=%s' % (obj.media.name)
            
        response['X-SendFile'] = str(obj.media.name)
        return response

#FIXME TBD
class BroadcastTable(tables.Table):
    class Meta:
        model = Broadcast
        attrs = {'class': 'paleblue'}
        #FIXME
        is_paginated = 'True'
        table_pagination = {
                    'per_page': 2
                }

import django_filters
class BroadcastFilter(django_filters.FilterSet):
    class Meta:
        model = Broadcast
        fields = ['name', 'description']
        
class BroadcastFilterFormHelper():
    class Meta:
        model = Broadcast
    
        
class BroadcastTableView(TemplateView):
    template_name = 'broadcast_list.html'

    def get_queryset(self, **kwargs):
        return Broadcast.objects.all()

    def get_context_data(self, **kwargs):
        context = super(BroadcastTableView, self).get_context_data(**kwargs)
        filter = BroadcastFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        filter.form.helper = BroadcastFilterFormHelper()
        table = BroadcastTable(filter.qs)
        RequestConfig(self.request).configure(table)
        context['filter'] = filter
        context['table'] = table
        return context
#FIXME ENDTBD
    
class BroadcastListView(ListView):
    model = Broadcast

    template_name = 'django-tables2_list.html'

    def get_context_data(self, **kwargs):
        context = super(BroadcastListView, self).get_context_data(**kwargs)
        # print(context)
        qs = self.get_queryset()
        context['queryset'] = qs

        table = BroadcastTable(qs)
        RequestConfig(self.request).configure(table)
        context['table'] = table
        
        return context
    
    '''
    def get(self, request):
        qs = super(BroadcastListView, self).get_queryset()

        table = BroadcastTable(qs)
        RequestConfig(request).configure(table)
        # table.paginate(page=request.GET.get('page', 1), per_page=2)
            
        # print('Table[%s]' % qs)
        # return HttpResponse(table)
        return render(request, 'django-tables2_list.html', {'table': table})
    '''    

    def get_queryset(self):
        qs = super(BroadcastListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(name__icontains=query)|
                Q(description__icontains=query)
            ).order_by('-pk')  # '-name' etc  Default perhaps is 'name'

        return qs # .filter(name__icontains='adsfs')


class SerializerList(generics.ListCreateAPIView):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer

class SerializerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer

class SerializerDetailSlug(generics.RetrieveUpdateDestroyAPIView):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer
    lookup_field = 'slug'

