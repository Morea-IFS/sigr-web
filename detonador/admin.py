from django.contrib import admin
from .models import DetonadorEvento


class DetonadorEventoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_devices', 'delay_ms', 'pin_sequence', 'is_active']
    list_filter = ['devices', 'is_active']
    search_fields = ['name']
    
    def get_devices(self, obj):
        return ", ".join([d.name for d in obj.devices.all()])
    get_devices.short_description = 'Dispositivos'
    
admin.site.register(DetonadorEvento, DetonadorEventoAdmin)