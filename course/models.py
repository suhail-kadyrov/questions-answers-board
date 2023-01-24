from django.db import models

from authentication.models import CustomUser
# from course.querysets.queryset import *

class Course(models.Model):
    name = models.CharField(max_length=150)
    semester = models.CharField(max_length=150)
    is_completed = models.BooleanField(default=False)
    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='professor')
    started_at = models.DateField()
    token = models.CharField(max_length=150, null=False)
    students = models.ManyToManyField(CustomUser, related_name='course', blank=True)

    # objects = CourseManager()

    def __str__(self):
        return self.name
