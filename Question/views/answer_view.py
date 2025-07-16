from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from Question.models.answer import Answer
from Question.serilizers.answer_ser import (
    AnswerListSerializer,
    AnswerCreateSerializer,
    AnswerDetailSerializer,
    AnswerUpdateSerializer
)

class AnswerListCreateView(APIView):
    def get(self, request):
        answers = Answer.objects.select_related('question').all()
        serializer = AnswerListSerializer(answers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=AnswerCreateSerializer,
        responses={201: AnswerCreateSerializer}
    )
    def post(self, request):
        serializer = AnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AnswerDetailView(APIView):
    def get(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        serializer = AnswerDetailSerializer(answer)
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body=AnswerUpdateSerializer,
        responses={201: AnswerUpdateSerializer}
    )
    def put(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        if(answer.user!=request.user):
            return Response(
                {'message': 'You are not allowed to update this Answer.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = AnswerUpdateSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        if(answer.user!=request.user):
            return Response(
                {'message': 'You are not allowed to update this question.'},
                status=status.HTTP_403_FORBIDDEN
            )
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
