from django.db import models
from django.contrib.auth.models import User

class QRCodeType(models.Model):
    name = models.CharField(max_length=100)
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name

class QRCode(models.Model):
    name = models.CharField(max_length=150)
    information = models.JSONField()
    owner = models.ForeignKey(User, related_name="qr_codes", on_delete=models.CASCADE, null=True)
    qr_type = models.ForeignKey(QRCodeType, related_name="qr_codes", on_delete=models.SET_NULL, null=True, blank=True)
    download_count = models.IntegerField(default=0)
    border = models.IntegerField(default=1, null=True, blank=True)
    scale = models.IntegerField(default=4, null=True, blank=True)
    unit = models.CharField(max_length=10, default='mm', null=True, blank=True)
    dark = models.CharField(max_length=20, default='black', null=True, blank=True)
    light = models.CharField(max_length=20, default='white', null=True, blank=True)
    data_dark = models.CharField(max_length=20, null=True, blank=True)
    data_light = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name