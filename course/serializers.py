from rest_framework import serializers
from uuid import uuid4
from authentication.models import *
from course.models import *

class GetUser(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
class CoursesListSerializers(serializers.ModelSerializer):
    professor = GetUser(read_only=True)
    class Meta:
        model = Course
        fields = ['id','name','semester','started_at','is_completed','professor',]

class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','name','semester','started_at','is_completed',]

    def create(self,validated_date):
        create_course = Course.objects.create(
            name = validated_date['name'],
            semester = validated_date['semester'],
            started_at = validated_date['started_at'],
            professor = self.context.get('user_id')
        )
        new_token = uuid4()
        while bool(Course.objects.filter(token=new_token)):
            new_token = uuid4()
        create_course.token = new_token
        create_course.save()
        return create_course
    def update(self,instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.semester = validated_data.get('semester',instance.semester)
        instance.is_completed = validated_data['is_completed',instance.is_completed]
        instance.save()
        return instance