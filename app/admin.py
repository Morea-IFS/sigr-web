from django.contrib import admin
from .models import Device


class DevicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'application', 'mac_address', 'ip_address', 'is_authorized']
    
admin.site.register(Device, DevicesAdmin)