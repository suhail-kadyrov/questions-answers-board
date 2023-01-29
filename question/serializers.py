from dataclasses import fields

from rest_framework import serializers

import question
from question.models import Question


class QuestionRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question',]
