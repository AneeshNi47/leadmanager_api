from django.db import models
from django.contrib.auth.models import User


class LeadStatus(models.Model):
    status_title = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    active = models.BooleanField()
class Lead(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=254)
    message = models.CharField(max_length=500, blank=True)
    status = models.ForeignKey(LeadStatus, related_name="leads", on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, related_name="leads", on_delete=models.CASCADE, null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)