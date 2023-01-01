# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/notifications/admin/", consumers.AdminConsumer.as_asgi()),
    path("ws/notifications/professor/<int:id>/", consumers.ProfessorConsumer.as_asgi()),
    path("ws/notifications/student/<int:id>/", consumers.StudentConsumer.as_asgi()),
]