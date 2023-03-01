from chat.models import Thread
from chat.serializers import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from profiles.permissions import IsVerifiedUser
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response

from course.models import *
from course.querysets.queryset import (get_answered_questions,
                                       get_given_questions)
from course.serializers import *


class CourseListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]
    serializer_class = CoursesListSerializers

    def get(self, request, format=None):
        search_term = request.query_params.get('search', '')
        user = request.user
        if user.role == 'STUDENT':
            courses = user.enrolled_courses.all().filter(Q(name__icontains=search_term) | Q(semester__icontains=search_term))
        else:
            courses = Course.objects.filter(Q(professor=user) & (Q(name__icontains=search_term) | Q(semester__icontains=search_term)))
        courses = courses.order_by('-id')
        response = list(
            map(
                lambda course: {**course, 'given_questions': get_given_questions(course['id'], user), 'answered': get_answered_questions(course['id'], user)},
                self.serializer_class(courses, many=True).data
            )
        )
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if request.user == 'STUDENT':
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        serializers = CourseSerializer(data=request.data, context={'user': request.user})
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)


class CourseDetailView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ThreadSerializer

    def get(self, request, pk, format=None):
        user = request.user
        course = get_object_or_404(Course, pk=pk)
        threads = Thread.objects.filter(course=course)
        if user.role == 'STUDENT':
            threads = threads.filter(student=user)
        threads = threads.order_by('-id')
        thread_serializer = self.serializer_class(threads, many=True)
        course_serializer = CoursesListSerializers(course)
        return Response({
            'course': course_serializer.data,
            'threads': thread_serializer.data
        })

    def patch(self, request, pk):
        course = get_object_or_404(Course, pk=pk, professor=request.user)
        try:
            course.students.add(*request.data['students'])
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            course.save()
            students = CustomUser.objects.filter(id__in=request.data['students'])
            notification = list(map(
                lambda s: Notification(
                    name='STUDENT_INVITED',
                    text=f'{course.professor.full_name} has invited you to {course.name}',
                    receiver=s,
                    user=course.professor,
                    course=course,
                ),
                students
            ))
            Notification.objects.bulk_create(notification)
            return Response({'students': course.students.count()}, status=status.HTTP_200_OK)


class StudentsListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='STUDENT')
    serializer_class = ProfileSerializer


class CourseStudentsListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    
    def get_queryset(self):
        return get_object_or_404(Course, id=self.kwargs['course_id']).students.all()


class ExploreNewCoursesView(generics.ListAPIView):
    serializer_class = CoursesListSerializers
    filter_backends = [filters.SearchFilter,]
    search_fields = ['name', 'semester', '=professor__email']

    def get_queryset(self):
        return Course.objects.filter(is_completed=False).exclude(id__in=self.request.user.enrolled_courses.all())
