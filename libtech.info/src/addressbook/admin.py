from django.contrib import admin

# Register your models here.

from .models import AddressBook

class AddressBookAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['name']
    list_editable = ['description']
    class Meta:
        model = AddressBook
        

admin.site.register(AddressBook, AddressBookAdmin)
