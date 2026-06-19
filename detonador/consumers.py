import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DetonatorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.group_name = f'detonator_device_{self.device_id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_event(self, event):
        event_data = event
        raw_sequence = event_data['pin_sequence']
        pins_array = []
        if raw_sequence:
            for step in raw_sequence.split(','):
                group = [int(p) for p in step.split('+') if p.strip()]
                if group:
                    pins_array.append(group)
        
        message_to_send = {
            'type': 'event.trigger',
            'delay_ms': event_data['delay_ms'], 
            'pins': pins_array
        }
        await self.send(text_data=json.dumps(message_to_send))