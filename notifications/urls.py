# chat/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.NotificationListView.as_view(), name="new"),
    path("<str:room_name>/<int:id>/", views.room, name="room"),
]