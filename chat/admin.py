from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *
from .serializers import ThreadSerializer

# Register your models here.
admin.site.register(Thread)
admin.site.register(Message)

@receiver(post_save, sender=Thread)
def create_thread(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = f'PROFESSOR_{instance.course.professor.id}'
        serializer = ThreadSerializer(instance)
        async_to_sync(channel_layer.group_send)(
            group_name, {
                'type': 'chat_message',
                'data': {
                    "type": "THREAD",
                    "data": serializer.data
                }
            }
        )
