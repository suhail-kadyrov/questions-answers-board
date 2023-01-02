from django.contrib import admin
from course.models import *

@admin.register(Course)
class CourseViewsAdmin(admin.ModelAdmin):
    list_display = ['name','id','semester',]