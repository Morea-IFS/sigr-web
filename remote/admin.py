from django.contrib import admin
from .models import Remote, Button

class ButtonInline(admin.TabularInline):
    model = Button
    extra = 0 

class RemoteAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'device', 'button_count']
    inlines = [ButtonInline] 

    def button_count(self, obj):
        return obj.buttons.count()
    button_count.short_description = 'Botões Cadastrados'

admin.site.register(Remote, RemoteAdmin)
