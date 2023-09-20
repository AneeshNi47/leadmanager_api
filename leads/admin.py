from django.contrib import admin

from django.contrib import admin
from .models import Lead, LeadStatus

admin.site.register(LeadStatus)
admin.site.register(Lead)