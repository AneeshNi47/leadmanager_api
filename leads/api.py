from .models import Lead, LeadStatus
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
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
            # Get IDs of all superusers except the current user
            other_superuser_ids = User.objects.filter(is_superuser=True).exclude(id=self.request.user.id).values_list('id', flat=True)
            
            # Get all leads that aren't owned by the other superusers
            return Lead.objects.exclude(owner_id__in=other_superuser_ids)
        else:
            if self.request.user.is_authenticated:
                return self.request.user.leads.all()
            else:
                return Lead.objects.none()

    def perform_create(self, serializer):
        try:
            print("Creating new lead")
            new_lead_status = LeadStatus.objects.get(status_title="New Lead")
        except LeadStatus.DoesNotExist as error:
            raise ValidationError("The 'New Lead' status does not exist. Please create it first.")
        
        serializer.save(owner=self.request.user, status=new_lead_status)


    def perform_update(self, serializer):
        instance = self.get_object()

        # Check if the user is the owner or an admin
        if self.request.user == instance.owner or self.request.user.is_superuser:
            serializer.save()
        else:
            raise permissions.PermissionDenied("You do not have permission to update this Lead.")
