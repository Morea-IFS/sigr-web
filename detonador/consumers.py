import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DetonatorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Pega o ID do dispositivo da URL
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.group_name = f'detonator_device_{self.device_id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
        print(f"Dispositivo {self.device_id} conectado ao WebSocket e adicionado ao grupo {self.group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print(f"Dispositivo {self.device_id} desconectado.")

    async def send_event(self, event):
        event_data = event
        
        message_to_send = {
            'type': 'event.trigger',
            'delay_ms': event_data['delay_ms'], 
            'pins': [int(p) for p in event_data['pin_sequence'].split(',')]
        }
        await self.send(text_data=json.dumps(message_to_send))
        print(f"Evento enviado para o dispositivo {self.device_id}: {message_to_send}")

