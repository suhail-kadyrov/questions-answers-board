from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from profiles.permissions import IsVerifiedUser
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from chat.models import Message, Thread
from chat.serializers import *


class ThreadDetailView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]
    serializer_class = MessageSerializer

    def get(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        messages = Message.objects.filter(thread=thread).order_by('id')
        serializer = self.serializer_class(messages, many=True)
        return Response(serializer.data)
    

class ThreadCreateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]
    serializer_class = ThreadSerializer

    def post(self, request, format=None):
        serializers = self.serializer_class(data=request.data, context={'user': request.user})
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)


class MessageCreateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]
    serializer_class = MessageCreateSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = Message.objects.create(
            thread=serializer.validated_data['thread'],
            text=serializer.validated_data['text'],
            sender=request.user,
            reply_to_message=serializer.validated_data['reply_to_message'],
        )
        answer = None
        channel_layer = get_channel_layer()
        if message.sender.role == 'PROFESSOR':
            if message.reply_to_message:
                question = Question.objects.get(question=message.reply_to_message.text)
                question.answer = message.text
                question.save()
                Notification.objects.create(
                    name='STUDENT_NEW_ANSWER',
                    text=f'You have new answer in {message.thread.course.name}',
                    receiver=message.thread.student,
                    user=message.sender,
                    course=message.thread.course,
                    message=message
                )
            group_name = f'STUDENT_{message.thread.student.id}'
        else:
            question, created_ = Question.objects.get_or_create(question=message.text, professor=message.thread.course.professor)
            if not created_ and question.answer and not AutoAnswerSetting.objects.first().is_off:
                answer = Message.objects.create(
                    thread=message.thread,
                    text=question.answer,
                    sender=message.thread.course.professor,
                    reply_to_message=message
                )
                answer_serializer = MessageSerializer(answer)
                answer = answer_serializer.data
            else:
                Notification.objects.create(
                    name='PROFESSOR_NEW_QUESTION',
                    text=f'You have new question in {message.thread.course.name}',
                    receiver=message.thread.course.professor,
                    user=message.sender,
                    course=message.thread.course,
                    message=message
                )
            group_name = f'PROFESSOR_{message.thread.course.professor.id}'
        serializer = MessageSerializer(message)
        async_to_sync(channel_layer.group_send)(
            group_name, {
                'type': 'chat_message',
                'data': {
                    "type": "MESSAGE",
                    "data": serializer.data
                }
            }
        )
        if answer:
            async_to_sync(channel_layer.group_send)(
                group_name, {
                    'type': 'chat_message',
                    'data': {
                        "type": "MESSAGE",
                        "data": answer_serializer.data
                    }
                }
            )
        return Response({'data': serializer.data, 'answer': answer}, status=status.HTTP_200_OK)


class MessageUpdateDestroyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsVerifiedUser]
    serializer_class = MessageUpdateSerializer

    def put(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = Message.objects.get(id=pk)
        message.text = serializer.validated_data['text']
        message.is_edited = True
        message.save()

        answer = None
        channel_layer = get_channel_layer()
        if message.sender.role == 'PROFESSOR':
            if message.reply_to_message:
                question = Question.objects.get(question=message.reply_to_message.text)
                question.answer = message.text
                question.save()
            group_name = f'STUDENT_{message.thread.student.id}'
        else:
            question, created_ = Question.objects.get_or_create(question=message.text, professor=message.thread.course.professor)
            if not created_ and question.answer and not AutoAnswerSetting.objects.first().is_off:
                answer = Message.objects.create(
                    thread=message.thread,
                    text=question.answer,
                    sender=message.thread.course.professor,
                    reply_to_message=message
                )
                answer_serializer = MessageSerializer(answer)
                answer = answer_serializer.data
            group_name = f'PROFESSOR_{message.thread.course.professor.id}'
        serializer = MessageSerializer(message)
        async_to_sync(channel_layer.group_send)(
            group_name, {
                'type': 'chat_message',
                'data': {
                    "type": "EDITED_MESSAGE",
                    "data": serializer.data
                }
            }
        )
        if answer:
            async_to_sync(channel_layer.group_send)(
                group_name, {
                    'type': 'chat_message',
                    'data': {
                        "type": "MESSAGE",
                        "data": answer_serializer.data
                    }
                }
            )
        return Response({'data': serializer.data, 'answer': answer}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        message = Message.objects.get(id=pk)

        channel_layer = get_channel_layer()
        if message.sender.role == 'PROFESSOR':
            group_name = f'STUDENT_{message.thread.student.id}'
        else:
            group_name = f'PROFESSOR_{message.thread.course.professor.id}'
        message.delete()
        async_to_sync(channel_layer.group_send)(
            group_name, {
                'type': 'chat_message',
                'data': {
                    "type": "DELETED_MESSAGE"
                }
            }
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
