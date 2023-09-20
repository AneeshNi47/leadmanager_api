from .models import Lead, LeadStatus
from rest_framework import viewsets, permissions
from .serializers import LeadSerializer, LeadStatusSerializer


class LeadStatusViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = LeadStatusSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
                return LeadStatus.objects.all()
        else:
                return LeadStatus.objects.none()
        
class LeadViewSet(viewsets.ModelViewSet):
    permission_classes = [
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

    def perform_update(self, serializer):
        instance = self.get_object()

        # Check if the user is the owner or an admin
        if self.request.user == instance.owner or self.request.user.is_superuser:
            serializer.save()
        else:
            raise permissions.PermissionDenied("You do not have permission to update this Lead.")
