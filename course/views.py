from os import stat

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,authentication,permissions
from django.shortcuts import get_list_or_404
from course.models import *
from course.serializers import *



class CourseViews(APIView):
    def get(self,request,format=None):
        courses = Course.objects.courses(request.user)
        serializers = CoursesListSerializers(courses,many=True)
        return Response({'data':serializers.data},status=status.HTTP_200_OK)

    def post(self,request,format=None):
        serializers = CourseSerializers(data=request.data,context={'user_id':request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'success','data':serializers.data},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class CourseListViews(APIView):
    def get(self,request,pk,format=None):
        course_list = Course.objects.course_list(pk)
        serializers = CoursesListSerializers(course_list, many=True)
        return Response({'data': serializers.data}, status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        serializers = CourseSerializers(instance=Course.objects.filter(id=pk)[0], data=request.user.id, partial=True,context={'user_id':request.user.id})
        print(serializers.is_valid())
        if serializers.is_valid(raise_exception=True):
            print('is')
            serializers.save()
            return Response({'message': "success update"}, status=status.HTTP_200_OK)
        return Response({'error': 'update error data'}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        course_list = Course.objects.course_list(pk)
        course_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

