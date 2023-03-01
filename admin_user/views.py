from authentication.models import *
from course.models import Course
from course.serializers import CoursesListSerializers
from django.shortcuts import get_object_or_404
from profiles.permissions import IsVerifiedUser
from rest_framework import filters, generics, permissions, views
from rest_framework.response import Response

from .models import AutoAnswerSetting
from .permissions import IsAdmin
from .serializers import *


class AdminCoursesListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CoursesListSerializers
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsAdmin]
    filter_backends = [filters.SearchFilter,]
    search_fields = ['name', 'semester', '=professor__email']


class AdminProfessorsListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='PROFESSOR')
    serializer_class = UsersListSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsAdmin]
    filter_backends = [filters.SearchFilter,]
    search_fields = ['full_name', 'email',]


class AdminStudentsListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='STUDENT')
    serializer_class = UsersListSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsAdmin]
    filter_backends = [filters.SearchFilter,]
    search_fields = ['full_name', 'email',]


class LoginAttemptsListView(generics.ListAPIView):
    queryset = LoginAttempt.objects.all()
    serializer_class = LoginAttemptsSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsAdmin]


class AutoAnswerSettingsView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsAdmin]

    def get(self, request):
        is_off = AutoAnswerSetting.objects.first().is_off
        return Response({'is_off': is_off})
    
    def post(self, request):
        auto_answer_setting = AutoAnswerSetting.objects.first()
        auto_answer_setting.is_off = not auto_answer_setting.is_off
        auto_answer_setting.save()
        return Response({'is_off': auto_answer_setting.is_off})


class AdminCourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = AdminCourseDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsAdmin]


class AdminUserDestroyView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsAdmin]


class AdminProfessorCoursesListView(generics.ListAPIView):
    serializer_class = CoursesListSerializers
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsAdmin]

    def get_queryset(self):
        return Course.objects.filter(professor=self.kwargs['pk'])


class AdminStudentCoursesListView(generics.ListAPIView):
    serializer_class = CoursesListSerializers
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser, IsAdmin]

    def get_queryset(self):
        student = get_object_or_404(CustomUser, id=self.kwargs['pk'])
        return student.enrolled_courses.all()
