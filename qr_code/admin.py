from django.contrib import admin

from django.contrib import admin
from .models import QRCode, QRCodeType

admin.site.register(QRCode)
admin.site.register(QRCodeType)