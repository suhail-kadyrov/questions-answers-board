from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from course.models import *

class CourseQuerySet(QuerySet):
    def courses(self,user):
        list_course = []
        for item in self.filter(professor=user.id,professor__role='PROFESSOR'):
            list_course.append({
                'id':item.id,
                'name': item.name,
                'semester':item.semester,
                'is_complated':item.is_completed,
                'started_at':item.started_at,
            })
        return list(list_course)

    def course_list(self,id):
        return self.filter(id=id)

class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model,using=self.db)

    def courses(self,user):
        return self.get_queryset().courses(user)

    def course_list(self,id):
        return self.get_queryset().course_list(id)