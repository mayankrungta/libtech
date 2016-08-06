from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import get_object_or_404

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)

class MultiSlugMixin(object):
    model = None
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        ModelClass = self.model
        print('slug[%s]' % slug)

        if slug:
            try:
                obj = get_object_or_404(ModelClass, slug=slug)
            except ModelClass.MultipleObjectsReturned:
                obj = ModelClass.objects.filter(slug=slug).order_by('-title').first()
        else:
            obj = super(MultiSlugMixin, self).get_object()
        return obj

class SubmitButtonMixin(object):
    submit_btn = None
    
    def get_context_data(self, **kwargs):
        context = super(SubmitButtonMixin, self).get_context_data(**kwargs)
        context['submit_btn'] = 'Add Product'
        return context

