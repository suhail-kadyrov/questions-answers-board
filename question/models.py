from django.db import models
from authentication.models import CustomUser

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=2048)
    answer = models.CharField(max_length=2048)
    professor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
