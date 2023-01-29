from chat.models import *
from course.models import Course
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet


class CourseQuerySet(QuerySet):
    def courses(self,user):
        list_course = []
        for item in self.filter(professor=user.id, professor__role='PROFESSOR'):
            list_course.append({
                'id':item.id,
                'name': item.name,
                'semester':item.semester,
                'is_complated':item.is_completed,
                'started_at':item.started_at
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


def get_given_questions(course_id, user):
    course = Course.objects.filter(id=course_id)
    if course.exists():
        course = course.first()
    else:
        return 0
    if user.role == 'STUDENT':
        threads = Thread.objects.filter(course=course, student=user)
        messages = Message.objects.filter(thread__in=threads, sender=user)
    else:
        threads = Thread.objects.filter(course=course)
        messages = Message.objects.filter(thread__in=threads, sender__role='STUDENT')
    return messages.count()


def get_answered_questions(course_id, user):
    course = Course.objects.filter(id=course_id)
    if course.exists():
        course = course.first()
    else:
        return 0
    if user.role == 'STUDENT':
        threads = Thread.objects.filter(course=course, student=user)
        messages = Message.objects.filter(thread__in=threads).exclude(sender=user)
    else:
        threads = Thread.objects.filter(course=course)
        messages = Message.objects.filter(thread__in=threads, sender__role='PROFESSOR')
    return messages.count()
