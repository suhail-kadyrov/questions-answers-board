from django.urls import path
from course.views import *


urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
]