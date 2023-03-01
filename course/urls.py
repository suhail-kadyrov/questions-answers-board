from django.urls import path

from course.views import *

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
    path('explore/', ExploreNewCoursesView.as_view()),
    path('students/', StudentsListView.as_view()),
    path('course_students/<int:course_id>/', CourseStudentsListView.as_view()),
]
