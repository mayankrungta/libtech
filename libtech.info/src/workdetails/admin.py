from django.contrib import admin

# Register your models here.
from .models import Workdetail, MyWorkdetails

class WorkdetailAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'block_name', 'panchayat_name', 'financial_year', 'muster_index', 'is_closed', 'remarks']
    search_fields = ['block_name', 'name']
    list_filter = ['block_name', 'panchayat_name']
    list_editable = ['name', 'is_closed', 'remarks']
    class Meta:
        model = Workdetail

admin.site.register(Workdetail, WorkdetailAdmin)
admin.site.register(MyWorkdetails)
