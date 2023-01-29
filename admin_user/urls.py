from django.urls import path

from .views import *

urlpatterns = [
    path('courses/', AdminCoursesListView.as_view()),
    path('professors/', AdminProfessorsListView.as_view()),
    path('professor/<int:pk>/', AdminProfessorCoursesListView.as_view()),
    path('students/', AdminStudentsListView.as_view()),
    path('student/<int:pk>/', AdminStudentCoursesListView.as_view()),
    path('auto_answer/', AutoAnswerSettingsView.as_view()),
    path('course/<int:pk>/', AdminCourseDetailView.as_view()),
    path('user/<int:pk>/', AdminUserDestroyView.as_view()),
    # path('<int:pk>/', CourseDetailView.as_view()),
    # path('students/', StudentsListView.as_view()),
]
