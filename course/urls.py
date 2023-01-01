from django.urls import path
from course.views import *


urlpatterns = [
    path('',CourseViews.as_view()),
    path('course_list/<int:pk>/',CourseListViews.as_view()),
]