from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from Question.models.question import Question
from Question.serilizers.question_ser import (
    QuestionSerializer,
    QuestionCreateSerializer,
    QuestionDetailSerializer,
    QuestionUpdateSerializer,
)


class QuestionListCreateView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body=QuestionCreateSerializer,
        responses={201: QuestionCreateSerializer}
    )
    def post(self, request):
        serializer = QuestionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionUpdateDeleteView(APIView):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionDetailSerializer(question)
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body=QuestionUpdateSerializer,
        responses={201: QuestionUpdateSerializer}
    )
    def put(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionUpdateSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
