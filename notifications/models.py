from authentication.models import CustomUser
from chat.models import Course, Message
from django.db import models

# Create your models here.
NOTIFICATION_TYPES = (
    ('STUDENT_REQUEST_SENT', 'STUDENT_REQUEST_SENT'),
    ('STUDENT_REQUEST_ACCEPTED', 'STUDENT_REQUEST_ACCEPTED'),
    ('STUDENT_REQUEST_REJECTED', 'STUDENT_REQUEST_REJECTED'),
    ('STUDENT_INVITED', 'STUDENT_INVITED'),
    ('STUDENT_NEW_ANSWER', 'STUDENT_NEW_ANSWER'),
    ('PROFESSOR_NEW_QUESTION', 'PROFESSOR_NEW_QUESTION'),
    ('PROFESSOR_ENROLMENT_REQUEST', 'PROFESSOR_ENROLMENT_REQUEST'),
    ('PROFESSOR_PROMOTION_SENT', 'PROFESSOR_PROMOTION_SENT'),
    ('PROFESSOR_PROMOTION_ACCEPTED', 'PROFESSOR_PROMOTION_ACCEPTED'),
    ('PROFESSOR_PROMOTION_REJECTED', 'PROFESSOR_PROMOTION_REJECTED'),
    ('ADMIN_NEW_COURSE', 'ADMIN_NEW_COURSE'),
    ('ADMIN_NEW_ENROLMENT', 'ADMIN_NEW_ENROLMENT'),
    ('ADMIN_PROMOTION_REQUEST', 'ADMIN_PROMOTION_REQUEST'),
)

class Notification(models.Model):
    name = models.CharField(max_length=32, choices=NOTIFICATION_TYPES)
    text = models.CharField(max_length=1024)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    sent_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    is_seen = models.BooleanField(default=False)
