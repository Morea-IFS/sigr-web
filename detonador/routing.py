from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/detonator/(?P<device_id>\w+)/$', consumers.DetonatorConsumer.as_asgi()),
]
