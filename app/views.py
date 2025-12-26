from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
import json
from rest_framework.response import Response
from rest_framework import status
import uuid
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as loginAuth
from .models import Device, DeviceApplication, AuthTypes
import logging

logger = logging.getLogger(__name__)

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            loginAuth(request, user)
            try:
                return redirect("/")
            except:
                return redirect('/')
        else:
            return render(request, 'login.html', {'invalid': 'Usuário ou senha inválidos'})   
    return render(request, 'login.html')

@api_view(['POST'])
def authenticateDevice(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            macAddress = data['macAddress']
            deviceIp = data['deviceIp']
            
            logger.info(f"Authentication request from MAC: {macAddress}, IP: {deviceIp}")
            if Device.objects.filter(mac_address=macAddress).exists():
                device = Device.objects.get(mac_address=macAddress)
                if device.is_authorized != AuthTypes.Authorized:
                    logger.warning(f"Device {macAddress} is not authorized. Status: {device.is_authorized}")
                    return Response({
                        'error': 'Device not authorized',
                        'status': device.is_authorized
                    }, status=status.HTTP_403_FORBIDDEN)
                    
                apiToken = uuid.uuid4()
                old_ip = device.ip_address
                device.api_token = str(apiToken)
                device.ip_address = deviceIp  
                device.save()
                
                logger.info(f"Device updated: {device.name}. IP changed from {old_ip} to {deviceIp}")
                
                return Response({
                    'api_token': apiToken, 
                    'id': device.id, 
                    'deviceName': device.name
                }, status=status.HTTP_200_OK)
            else:
                apiToken = uuid.uuid4()
                
                try:
                    name_suffix = macAddress[-6:].replace(':', '')
                    newDevice = Device(
                        name=f"New-Device-{name_suffix}",
                        mac_address=macAddress, 
                        ip_address=deviceIp, 
                        api_token=str(apiToken),
                        application=DeviceApplication.none, 
                        is_authorized=AuthTypes.pending  
                    )
                    newDevice.save()
                    logger.info(f"New pending device created: {newDevice.name} with IP: {deviceIp}")
                    
                except Exception as e:
                    logger.error(f"Error creating device: {str(e)}")
                    return Response({
                        'error': f'Something went wrong while creating device: {str(e)}'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({
                    'error': 'Device pending authorization',
                    'status': AuthTypes.pending
                }, status=status.HTTP_403_FORBIDDEN) 
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON in authentication request")
            return Response({
                'error': 'Invalid JSON format'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except KeyError as e:
            logger.error(f"Missing field in request: {str(e)}")
            return Response({
                'error': f'Missing required field: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Unexpected error in authenticateDevice: {str(e)}")
            return Response({
                'error': f'Internal server error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def offline_view(request):
    return render(request, 'offline.html')