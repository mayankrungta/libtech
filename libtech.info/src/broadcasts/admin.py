from django.contrib import admin

# Register your models here.
from .models import Broadcast, MyBroadcasts

class BroadcastAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'id', 'slug', 'description', 'start_time']
    search_fields = ['name', 'description']
    class Meta:
        model = Broadcast

admin.site.register(Broadcast, BroadcastAdmin)
admin.site.register(MyBroadcasts)
