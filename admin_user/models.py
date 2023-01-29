from django.db import models

# Create your models here.
class AutoAnswerSetting(models.Model):
    is_off = models.BooleanField(default=False)
