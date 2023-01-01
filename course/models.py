from django.db import models
from numpy.distutils.system_info import blas_info

from authentication.models import CustomUser
from course.querysets.queryset import *

class Course(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    semester = models.CharField(max_length=150, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    started_at = models.DateTimeField()
    token = models.CharField(max_length=150, null=False)

    objects = CourseManager()

    def __str__(self):
        return f"Course: {self.name} ,Semester: {self.semester}"
