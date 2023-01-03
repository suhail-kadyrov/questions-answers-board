from profiles.permissions import IsVerifiedUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from datetime import datetime, timedelta
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

from chat.models import *


# Create your views here.
class NotificationListView(generics.GenericAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    displayed_notifications_limit = 30

    def get(self, request):
        serializer = self.serializer_class(data=self.get_queryset(), many=True)
        serializer.is_valid()

        # Getting rid of expired notifications
        Notification.objects.filter(
            receiver=request.user,
            is_seen=True,
            sent_at__lte=datetime.now() - timedelta(days=90)
        ).delete()

        return Response(serializer.data)
    
    def get_queryset(self):
        notifications = Notification.objects.filter(receiver=self.request.user)
        not_seen = notifications.filter(is_seen=False)
        if not_seen.count() >= self.displayed_notifications_limit:
            return not_seen.order_by('-sent_at')
        seen = notifications.order_by('is_seen', '-sent_at')
        return seen[:self.displayed_notifications_limit]


# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "notifications/index.html")

def room(request, room_name, id):
    return render(request, "notifications/room.html", {"room_name": room_name})
