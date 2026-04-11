import requests
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Remote, Button, RemoteType
from app.models import Device, DeviceApplication

@login_required(login_url='/login')
def index(request):
    if request.method == 'POST':
        device_id = request.POST.get('device_id')
        name = request.POST.get('name')
        rtype = request.POST.get('type')
        dev = get_object_or_404(Device, id=device_id)
        Remote.objects.create(device=dev, name=name, type=rtype)
        return redirect('ir_dashboard')

    devices = Device.objects.filter(is_authorized=2)
    remotes = Remote.objects.filter(device__is_authorized=2)
    return render(request, 'dashboard.html', {
        'remotes': remotes, 'devices': devices, 'types': RemoteType.choices
    })

@login_required(login_url='/login')
def remote_interface(request, pk):
    remote = get_object_or_404(Remote, pk=pk)
    button_map = {btn.key_name: btn.id for btn in remote.buttons.all() if btn.key_name}
    
    return render(request, 'remotes.html', {
        'remote': remote,
        'button_map': button_map 
    })

@login_required
def trigger_signal(request, btn_id):
    button = get_object_or_404(Button, id=btn_id)
    ip = button.remote.device.ip_address 
    if not ip: return JsonResponse({'status': 'error', 'msg': 'Offline'})
    
    payload = {
    'protocol': button.protocol,
    'type': button.data_type,
    }

    if button.data_type == 'simple':
        payload.update({
            'value': button.code_value,
            'bits': button.bits
        })

    elif button.data_type == 'raw':
        payload.update({
            'raw': button.raw_data,
            'khz': 38
        })

    elif button.data_type == 'state':
        payload.update({
            'state': button.state_data
        })
    
    try:
        requests.post(f"http://{ip}/emit", json=payload, timeout=2)
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)})

@login_required
def start_learning(request, remote_id):
    remote = get_object_or_404(Remote, id=remote_id)
    ip = remote.device.ip_address
    key_name = request.GET.get('key', 'custom')
    label = request.GET.get('label', 'Botão')
    
    if not ip: return JsonResponse({'status': 'error', 'msg': 'Offline'})

    try:
        url = f"http://{ip}/learn?remote_id={remote.id}&btn_name={label}&key_name={key_name}"
        requests.get(url, timeout=3)
        return JsonResponse({'status': 'listening'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': str(e)})

@csrf_exempt
def save_learned_button(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
            print(f"DEBUG ESP: {data}") 

            remote_id = data.get('remote_id')
            btn_name = data.get('btn_name')
            key_name = data.get('key_name') 
            
            if not remote_id: return JsonResponse({'error': 'Missing remote_id'}, status=400)
            
            remote = get_object_or_404(Remote, id=remote_id)
            if key_name and key_name != 'custom':
                Button.objects.filter(remote=remote, key_name=key_name).delete()
            icon_class = "bi bi-circle"
            k = str(key_name).lower()
            if "power" in k: icon_class = "bi bi-power"
            elif "vol" in k: icon_class = "bi bi-soundwave"
            elif "temp" in k: icon_class = "bi bi-thermometer-half"
            elif "menu" in k: icon_class = "bi bi-list"

            new_btn = Button.objects.create(
                remote=remote,
                label=btn_name,
                key_name=key_name,
                icon=icon_class,
                protocol=data.get('protocol', 'UNKNOWN'),

                code_value=str(data.get('value', '0')),
                bits=data.get('bits', 0),
                data_type=data.get('type', 'simple'),
                raw_data=data.get('raw'),
                state_data=data.get('state'),
            )
            
            return JsonResponse({'status': 'saved', 'id': new_btn.id})
            
        except Exception as e:
            print(f"ERRO: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'status': 'method_not_allowed'}, status=405)

@csrf_exempt
@login_required
def update_ac_state(request, remote_id):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
            
            remote = get_object_or_404(Remote, id=remote_id)
            if 'is_on' in data:
                remote.ac_state_on = data['is_on']
            if 'temp' in data:
                remote.ac_current_temp = data['temp']
                
            remote.save()
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'status': 'method_not_allowed'}, status=405)