from functools import reduce

from admin_user.models import AutoAnswerSetting
from course.models import *
from django.db.models import Q
from django.shortcuts import get_object_or_404
from profiles.permissions import IsVerifiedUser
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from question.models import Question
from question.serializers import QuestionRecommendationSerializer


class QuestionRecommendationView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedUser]
    serializer_class = QuestionRecommendationSerializer

    def get_queryset(self):
        if AutoAnswerSetting.objects.first().is_off:
            return Question.objects.none()
        course_id = self.request.query_params.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        search = self.request.query_params.get('search')
        qs = Question.objects.filter(professor=course.professor).exclude(answer='')
        if search:
            search_query = reduce(
                lambda r, w: r & Q(question__icontains=w),
                [Q(question__icontains=''), *search.split(' ')]
            )
            qs = qs.filter(search_query)
        return qs[:5]
