from rest_framework import serializers
from .models import Remote, Button

class ButtonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Button
        fields = ['id', 'label', 'protocol', 'code_value', 'bits']

class RemoteSerializer(serializers.ModelSerializer):
    buttons = ButtonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Remote
        fields = ['id', 'name', 'type', 'buttons']