from django.db import models
from django.contrib.auth.models import User


class Lead(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, max_length=254)
    message = models.CharField(max_length=500, blank=True)
    owner = models.ForeignKey(User, related_name="leads", on_delete=models.CASCADE, null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)