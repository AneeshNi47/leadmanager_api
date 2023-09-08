from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Lead  # Replace with your actual model import

channel_layer = get_channel_layer()

# This will be triggered when a new Lead is created
@receiver(post_save, sender=Lead)
def announce_new_lead(sender, instance, created, **kwargs):
    if created:
        async_to_sync(channel_layer.group_send)(
            "leads",  # This is the name of the group you will send to, you should already have the same name when you connected to the WebSocket in your Consumer.
            {
                "type": "new.lead",
                "event": "New Lead",
                "lead_id": instance.id,
                "name": instance.name,
                "email": instance.email,
                "message": instance.message,
            },
        )

# This will be triggered when a Lead is deleted
@receiver(post_delete, sender=Lead)
def announce_deleted_lead(sender, instance, **kwargs):
    async_to_sync(channel_layer.group_send)(
        "leads",  # This is the name of the group you will send to
        {
            "type": "deleted.lead",
            "event": "Deleted Lead",
            "lead_id": instance.id,
        },
    )
