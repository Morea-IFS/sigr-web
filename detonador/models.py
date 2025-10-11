from django.db import models
from app.models import Device


class DetonadorEvento(models.Model):
    devices = models.ManyToManyField(Device)   
    name = models.CharField(max_length=100, default="Meu Evento")
    delay_ms = models.PositiveIntegerField(default=1000, help_text="Intervalo em milissegundos entre os acionamentos")
    pin_sequence = models.TextField(help_text="Sequência de Pinos, separados por vírgula. Ex: 5,7,1")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"Evento: {self.name}"