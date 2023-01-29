from authentication.models import CustomUser
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150)
    semester = models.CharField(max_length=150)
    is_completed = models.BooleanField(default=False)
    professor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    started_at = models.DateField()
    students = models.ManyToManyField(CustomUser, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.name
