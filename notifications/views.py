from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from rest_framework import generics
from rest_framework.response import Response

# Create your views here.
class NotificationListView(generics.GenericAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get(self, request):
        serializer = self.serializer_class(data=self.get_queryset(), many=True)
        serializer.is_valid()
        name = request.query_params.get('name')
        print(name)
        Notification.objects.create(name=name)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        Notification.objects.create(name=name)
        return Response({})

# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, "notifications/index.html")

def room(request, room_name, id):
    return render(request, "notifications/room.html", {"room_name": room_name})