from authentication.models import CustomUser
from course.models import Course
from django.db import models
from question.models import Question


# Create your models here.
class Thread(models.Model):
    title = models.ForeignKey(Question, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student')


class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    text = models.CharField(max_length=2048)
    sent_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_edited = models.BooleanField(default=False)
    reply_to_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True)
