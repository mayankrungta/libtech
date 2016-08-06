import os

from mimetypes import guess_type

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
#from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper  # For 1.9 upwards

from libtech.mixins import (
    LoginRequiredMixin,
    MultiSlugMixin,
    StaffRequiredMixin,
    SubmitButtonMixin,
)
from .models import Workdetail
from .form import WorkdetailAddForm, WorkdetailModelForm
from .mixins import WorkdetailManagerMixin
from .serializers import WorkdetailSerializer

#from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import generics
# Create your views here.

import django_tables2 as tables
from django_tables2 import RequestConfig, SingleTableView

class WorkdetailCreateView(LoginRequiredMixin, CreateView):
    model = Workdetail
    template_name = 'form.html'
    form_class = WorkdetailModelForm
    # success_url = '/workdetails/add/'
    submit_btn = 'Add Workdetail'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(WorkdetailCreateView, self).form_valid(form)
        form.instance.managers.add(user)
        form.instance.user.myworkdetails.workdetails.add(form.instance) # FIXME Mynk
        # Add all default users form.instance.managers.add('admin')
        
        return valid_data

    '''
    def get_success_url(self):
        return reverse('workdetails:list') # return '/users/%s/' % self.request.user
    '''
    
class WorkdetailUpdateView(WorkdetailManagerMixin, MultiSlugMixin, UpdateView):
    model = Workdetail
    template_name = 'form.html'
    form_class = WorkdetailModelForm
    #success_url = '/workdetails/'
    submit_btn = 'Update Workdetail'

class WorkdetailDetailView(MultiSlugMixin, DetailView):
    model = Workdetail
    
class WorkdetailDownloadView(MultiSlugMixin, DetailView):
    model = Workdetail

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj not in request.user.myworkdetails.workdetails.all():
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
    
class WorkdetailTable(tables.Table):
    class Meta:
        model = Workdetail
        attrs = {'class': 'paleblue'}
        #FIXME
        table_pagination = {
                    'per_page': 2
        }
        is_paginated = 'True'

class WorkdetailListView(ListView):
    model = Workdetail

    template_name = 'django-tables2_list.html'

    def get_context_data(self, **kwargs):
        context = super(WorkdetailListView, self).get_context_data(**kwargs)
        # print(context)
        qs = self.get_queryset()
        context['queryset'] = qs

        table = WorkdetailTable(qs)
        RequestConfig(self.request).configure(table)
        context['table'] = table
        
        return context

        # table.paginate(page=request.GET.get('page', 1), per_page=2)
            
        # print('Table[%s]' % qs)
        # return HttpResponse(table)
        return render(request, 'django-tables2_list.html', {'table': table})

    def get_queryset(self):
        qs = super(WorkdetailListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(panchayat_name__icontains=query)|
                Q(name__icontains=query)
            ).order_by('-pk')  # '-title' etc  Default perhaps is 'title'
        return qs # .filter(title__icontains='adsfs')



class SerializerList(generics.ListCreateAPIView):
    queryset = Workdetail.objects.all()
    serializer_class = WorkdetailSerializer

class SerializerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workdetail.objects.all()
    serializer_class = WorkdetailSerializer

class SerializerDetailSlug(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workdetail.objects.all()
    serializer_class = WorkdetailSerializer
    lookup_field = 'slug'
'''
Function Based Views vvv

'''
def create_view(request):
    import csv
    with open('./z.csv') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            i = 0
            while i < 38:
                if row[i] == 'None':
                    row[i] = None
                i += 1
                
            #print(row)
            _, created = Workdetail.objects.get_or_create(
                slug = row[0],
                block_name = row[1],
                block_code = row[2],
                panchayat_name = row[3],
                panchayat_code = row[4],
                financial_year = row[5],
                muster_index = row[6],
                name = row[7],
                jobcard = row[8],
                jobcard_number = row[9],
                muster_number = row[10],
                work_code = row[11],
                work_name = row[12],
                date_from = row[13],
                date_to = row[14],
                days_worked = row[15],
                day_wage = row[16],
                total_wage = row[17],
                account_number = row[18],
                wagelist_number = row[19],
                bank_or_po_name = row[20],
                branch_name_or_po_address = row[21],
                branch_or_po_code = row[22],
                status = row[23],
                credited_date = row[24],
                is_bank = row[25],
                is_post = row[26],
                rejection_reason = row[27],
                fto_event_date = row[28],
                fto_event = row[29],
                fto_office = row[30],
                fto_field = row[31],
                update_date = row[32],
                create_date = row[33],
                fto_number = row[34],
                fto_number_updated = row[35],
                primary_account_holder = row[36],
                payment_date = row[37],
                user = request.user,
            )
            
    template = 'workdetails/workdetail_list.html'
    context = {}
    return render(request, template, context)

def create_aliter_view(request):
    form = WorkdetailAddForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        data = form.cleaned_data
        obj = Workdetail()
        obj.title = data.get('title')
        obj.description = data.get('description')
        obj.price = data.get('price')
        obj.save()
        
    template = 'form.html'
    context = {'form': form, 'submit_btn': 'Create Workdetail', }
    return render(request, template, context)

def update_view(request, object_id=None):
    workdetail = get_object_or_404(Workdetail, id=object_id)
    form = WorkdetailModelForm(request.POST or None, instance=workdetail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        
    template = 'form.html'
    context = {'title': 'Detail', 'object': workdetail, 'form': form, 'submit_btn': 'Update Workdetail', }

    return render(request, template, context)


def detail_slug_view(request, slug=None):
    #print(slug)
    try:
        workdetail = get_object_or_404(Workdetail, slug=slug)
    except Workdetail.MultipleObjectsReturned:
        workdetail = Workdetail.objects.filter(slug=slug).order_by('-title').first()
        
        '''
    if not object_id:
        raise Http404

    try:
        workdetail = Workdetail.objects.get(id=object_id)
    except Workdetail.DoesNotExist:
        workdetail = None
    '''    
    template = 'detail_view.html'
    context = {'title': 'Detail', 'object': workdetail, }

    return render(request, template, context)

def detail_view(request, object_id=None):
    workdetail = get_object_or_404(Workdetail, id=object_id)
    '''
    if not object_id:
        raise Http404

    try:
        workdetail = Workdetail.objects.get(id=object_id)
    except Workdetail.DoesNotExist:
        workdetail = None
    '''    
    template = 'detail_view.html'
    context = {'title': 'Detail', 'object': workdetail, }

    return render(request, template, context)

def list_view(request):
    template = 'list_view.html'
    queryset = Workdetail.objects.all()
    context = {'queryset': queryset, }
    return render(request, template, context)
