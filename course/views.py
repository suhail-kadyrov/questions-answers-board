from chat.models import Message, Thread
from chat.serializers import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import (authentication, filters, generics, permissions,
                            status)
from rest_framework.response import Response

from course.models import *
from course.querysets.queryset import (get_answered_questions,
                                       get_given_questions)
from course.serializers import *


class CourseListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,) # IsProfessorOrReadOnly
    serializer_class = CoursesListSerializers

    def get(self, request, format=None):
        search_term = request.query_params.get('search', '')
        user = request.user
        if user.role == 'STUDENT':
            courses = user.course.all().filter(Q(name__icontains=search_term) | Q(semester__icontains=search_term))
        else:
            courses = Course.objects.filter(Q(professor=user) & (Q(name__icontains=search_term) | Q(semester__icontains=search_term)))
        response = list(
            map(
                lambda course: {**course, 'given_questions': get_given_questions(course['id'], user), 'answered': get_answered_questions(course['id'], user)},
                self.serializer_class(courses, many=True).data
            )
        )
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
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
        thread_serializer = self.serializer_class(threads, many=True)
        course_serializer = CoursesListSerializers(course)
        return Response({
            'course': course_serializer.data,
            'threads': thread_serializer.data
        })

    
    # def put(self,request,pk,format=None):
    #     course_list = Course.objects.filter(id=pk)[0]
    #     serializers = CourseSerializer(instance=course_list, data=request.data, partial=True)
    #     if serializers.is_valid(raise_exception=True):
    #         serializers.save()
    #         return Response({'message': "success update",'data':serializers.data}, status=status.HTTP_200_OK)
    #     return Response({'error': 'update error data'}, status=status.HTTP_400_BAD_REQUEST)
    
    # def delete(self,request,pk,format=None):
    #     course_list = Course.objects.course_list(pk).delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
