from django.db import models
from app.models import Device

class RemoteType(models.TextChoices):
    PR = 'PR', 'Projetor'
    AC = 'AC', 'Ar Condicionado'
    OTHER = 'OTHER', 'Outros'

class Remote(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='remotes')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=RemoteType.choices, default=RemoteType.OTHER)
    created_at = models.DateTimeField(auto_now_add=True)

    ac_state_on = models.BooleanField(default=False)
    ac_current_temp = models.IntegerField(default=20)

    def __str__(self):
        return f"{self.name} ({self.device.name})"

class Button(models.Model):
    remote = models.ForeignKey(Remote, on_delete=models.CASCADE, related_name='buttons')
    key_name = models.CharField(max_length=50, blank=True, null=True)
    
    label = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, default='bi bi-circle', blank=True)
    
    protocol = models.CharField(max_length=50)

    code_value = models.CharField(max_length=100, blank=True, null=True)
    bits = models.IntegerField(default=0)

    data_type = models.CharField(max_length=10, default='simple') 
    raw_data = models.JSONField(null=True, blank=True)
    state_data = models.JSONField(null=True, blank=True)