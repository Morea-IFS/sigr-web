from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DetonadorEvento
from app.models import Device
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required(login_url='/login')
def index(request):
    eventos = DetonadorEvento.objects.prefetch_related('devices').filter(devices__is_authorized=2, devices__application=2).distinct().order_by('name')

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'create_event':
            device_ids = request.POST.getlist('devices')
            nome_evento = request.POST.get('nome_evento')
            delay = request.POST.get('delay')
            pinos_selecionados = request.POST.getlist('pinos')

            if not all([device_ids, nome_evento, delay, pinos_selecionados]):
                messages.error(request, "Todos os campos são obrigatórios para criar um evento.")
            else:
                sequencia_str = ",".join(pinos_selecionados)
                novo_evento = DetonadorEvento.objects.create(
                    name=nome_evento,
                    delay_ms=int(delay),
                    pin_sequence=sequencia_str
                )
                novo_evento.devices.set(device_ids)
                messages.success(request, f"Evento '{nome_evento}' criado com sucesso!")
        
        elif action == 'edit_event':
            evento_id = request.POST.get('evento_id')
            device_ids = request.POST.getlist('devices')
            nome_evento = request.POST.get('nome_evento')
            delay = request.POST.get('delay')
            pinos_selecionados = request.POST.getlist('pinos')

            if not all([evento_id, device_ids, nome_evento, delay, pinos_selecionados]):
                messages.error(request, "Todos os campos são obrigatórios para editar o evento.")
            else:
                evento = get_object_or_404(DetonadorEvento, id=evento_id)
                evento.name = nome_evento
                evento.delay_ms = int(delay)
                evento.pin_sequence = ",".join(pinos_selecionados)
                evento.devices.set(device_ids) 
                evento.save()
                messages.success(request, f"Evento '{nome_evento}' atualizado com sucesso!")

        return redirect('detonador_dashboard')

    context = {
        'eventos': eventos,
        'devices': Device.objects.filter(is_authorized=2, application=2)
    }
    return render(request, 'dashboard/detonador.html', context)

@login_required(login_url='/login')
def activate_event(request, evento_id):
    evento_to_activate = get_object_or_404(DetonadorEvento, id=evento_id)
    devices_in_event = list(evento_to_activate.devices.all())
    channel_layer = get_channel_layer()
    async def send_event_to_devices():
        for device in devices_in_event:
            group_name = f'detonator_device_{device.id}'
            event_data = {
                'type': 'send.event',
                'delay_ms': evento_to_activate.delay_ms,
                'pin_sequence': evento_to_activate.pin_sequence,
            }

            print(f"Enviando para o grupo {group_name}: {event_data}")
            await channel_layer.group_send(group_name, event_data)

    async_to_sync(send_event_to_devices)()
    
    messages.success(request, f"Evento '{evento_to_activate.name}' detonado com sucesso!")
    return redirect('detonador_dashboard')


@login_required(login_url='/login')
def delete_event(request, evento_id):
    evento_to_delete = get_object_or_404(DetonadorEvento, id=evento_id)
    nome_evento = evento_to_delete.name
    evento_to_delete.delete()
    messages.warning(request, f"Evento '{nome_evento}' foi removido.")
    return redirect('detonador_dashboard')
