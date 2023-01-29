from django.urls import path

from chat.views import *

urlpatterns = [
    path('thread/', ThreadCreateView.as_view()),
    path('thread/<int:pk>/', ThreadDetailView.as_view()),
    path('message/', MessageCreateView.as_view()),
    path('message/<int:pk>/', MessageUpdateDestroyView.as_view()),
]
