from django.http import Http404

from libtech.mixins import LoginRequiredMixin

class WorkdetailManagerMixin(LoginRequiredMixin, object):
    def get_object(self, *args, **kwargs):
        user = self.request.user
        obj = super(WorkdetailManagerMixin, self).get_object(*args, **kwargs)

        try:
            user == obj.user
        except:
            raise Http404

        try:
            user in obj.managers.all()
        except:
            raise Http404
        
        if user == obj.user or user in obj.managers.all():
            return obj
        else:
            raise Http404
'''    
    def get_object(self, *args, **kwargs):
        user = self.request.user
        obj = super(WorkdetailUpdateView, self).get_object(*args, **kwargs)
        # print('user[%s], obj.user[%s], obj.managers.all[%s]' %(user, obj.user, obj.managers.all()))

        if user == obj.user or user in obj.managers.all():
            return obj
        else:
            raise Http404
'''
