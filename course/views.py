from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,authentication,permissions
from course.models import *
from course.serializers import *



class CourseViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,format=None):
        courses = Course.objects.courses(request.user)
        print(courses)
        serializers = CoursesListSerializers(courses,many=True)
        return Response({'data':serializers.data},status=status.HTTP_200_OK)

    def post(self,request,format=None):
        serializers = CourseSerializers(data=request.data,context={'user_id':request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'msg':'success','data':serializers.data},status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class CourseListViews(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,pk,format=None):
        course_list = Course.objects.course_list(pk)
        serializers = CoursesListSerializers(course_list, many=True)
        return Response({'data': serializers.data}, status=status.HTTP_200_OK)
    def put(self,request,pk,format=None):
        course_list = Course.objects.filter(id=pk)[0]
        serializers = CourseSerializers(instance=course_list, data=request.data, partial=True)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response({'message': "success update",'data':serializers.data}, status=status.HTTP_200_OK)
        return Response({'error': 'update error data'}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        course_list = Course.objects.course_list(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

