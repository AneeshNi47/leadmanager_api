from .models import Lead
from rest_framework import viewsets, permissions
from .serializers import LeadSerializer


class LeadViewSet(viewsets.ModelViewSet):
    permissions_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = LeadSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Lead.objects.all()
        else:
            if self.request.user.is_authenticated:
                return self.request.user.leads.all()
            else:
                return Lead.objects.none()  
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    