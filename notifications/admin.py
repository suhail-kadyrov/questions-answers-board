from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification
from .serializers import NotificationSerializer

# Register your models here.
admin.site.register(Notification)

@receiver(post_save, sender=Notification)
def create_profile(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = instance.name.split('_')[0]
        if group_name != 'ADMIN':
            group_name += '_{}'.format(instance.receiver.id)
        else:
            group_name = 'ADMIN_1'
        serializer = NotificationSerializer(instance)
        async_to_sync(channel_layer.group_send)(
            group_name, {
                'type': 'chat_message',
                'data': {
                    "type": "NOTIFICATION",
                    "data": serializer.data
                }
            }
        )
