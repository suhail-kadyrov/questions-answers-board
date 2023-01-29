from django.urls import path

from . import views

urlpatterns = [
    path('', views.QuestionRecommendationView.as_view())
]
