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
    
    
class WorkdetailListView(ListView):
    model = Workdetail
    '''
    template_name = 'list_view.html'

    def get_context_data(self, **kwargs):
        context = super(WorkdetailListView, self).get_context_data(**kwargs)
        print(context)
        context['queryset'] = self.get_queryset()
        return context
    '''
    def get_queryset(self):
        qs = super(WorkdetailListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query)|
                Q(description__icontains=query)
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
    form = WorkdetailModelForm(request.POST or None)
    template = 'form.html'
    
    if form.is_valid():
        instance = form.save(commit=False)

        user = request.user
        instance.user = user
        # instance.managers.add(user)
        # instance.user.myworkdetails.workdetails.add(form.instance) # FIXME Mynk
        # Add all default users form.instance.managers.add('admin')

        import csv
        with open('./z.csv') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                print(row)
                '''
                _, created = Workdetail.objects.get_or_create(
                                     row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                     row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19],
                                     row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29],
                                     row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37],                     
                )
                '''
                instance.slug = row[0]
                instance.block_name = row[1]
                instance.block_code = row[2]
                instance.panchayat_name = row[3]
                instance.panchayat_code = row[4]
                instance.financial_year = row[5]
                instance.muster_index = row[6]
                instance.name = row[7]
                instance.jobcard = row[8]
                instance.jobcard_number = row[9]
                instance.muster_number = row[10]
                instance.work_code = row[11]
                instance.work_name = row[12]
                instance.date_from = row[13]
                instance.date_to = row[14]
                instance.days_worked = row[15]
                instance.day_wage = row[16]
                instance.total_wage = row[17]
                instance.account_number = row[18]
                instance.wagelist_number = row[19]
                instance.bank_or_po_name = row[20]
                instance.branch_name_or_po_address = row[21]
                instance.branch_or_po_code = row[22]
                instance.status = row[23]
                instance.credited_date = row[24]
                instance.is_bank = row[25]
                instance.is_post = row[26]
                instance.rejection_reason = row[27]
                if row[28] == 'None':
                    instance.fto_event_date = None
                else:
                    instance.fto_event_date = row[28]
                instance.fto_event = row[29]
                instance.fto_office = row[30]
                instance.fto_field = row[31]
                instance.update_date = row[32]
                instance.create_date = row[33]
                instance.fto_number = row[34]
                instance.fto_number_updated = row[35]
                instance.primary_account_holder = row[36]
                instance.payment_date = row[37]
                instance.save()
            
                template = 'workdetails/workdetail_list.html'
    context = {'form': form, }
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
