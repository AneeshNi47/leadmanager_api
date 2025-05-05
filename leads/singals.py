from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from .models import Lead

# Safely get channel layer
channel_layer = get_channel_layer()

@receiver(post_save, sender=Lead)
def announce_new_lead(sender, instance, created, **kwargs):
    if created and channel_layer:
        try:
            async_to_sync(channel_layer.group_send)(
                "leads",
                {
                    "type": "new.lead",
                    "event": "New Lead",
                    "lead_id": instance.id,
                    "name": instance.name,
                    "email": instance.email,
                    "message": instance.message,
                },
            )
        except Exception as e:
            if settings.DEBUG:
                print("Channel error:", e)

@receiver(post_delete, sender=Lead)
def announce_deleted_lead(sender, instance, **kwargs):
    if channel_layer:
        try:
            async_to_sync(channel_layer.group_send)(
                "leads",
                {
                    "type": "deleted.lead",
                    "event": "Deleted Lead",
                    "lead_id": instance.id,
                },
            )
        except Exception as e:
            if settings.DEBUG:
                print("Channel error:", e)
