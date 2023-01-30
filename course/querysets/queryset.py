from chat.models import *
from course.models import Course


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
