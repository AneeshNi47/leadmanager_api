from rest_framework import serializers
from .models import Lead, LeadStatus

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model= Lead
        fields = '__all__'

class LeadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model= LeadStatus
        fields = '__all__'