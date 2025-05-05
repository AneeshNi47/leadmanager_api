from rest_framework import serializers
from .models import QRCode, QRCodeType

class QRCodeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model= QRCodeType
        fields = '__all__'

class QRCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QRCode
        fields = '__all__'
        extra_kwargs = {
            'qr_type': {'required': True, 'allow_null': False}
        }