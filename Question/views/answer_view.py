from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from Question.models.answer import Answer
from Question.serilizers.answer_ser import (
    AnswerListSerializer,
    AnswerCreateSerializer,
    AnswerDetailSerializer,
    AnswerUpdateSerializer
)

class AnswerListCreateView(APIView):
    def get(self, request):
        answers = Answer.objects.all()
        serializer = AnswerListSerializer(answers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AnswerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AnswerDetailView(APIView):
    def get(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        serializer = AnswerDetailSerializer(answer)
        return Response(serializer.data)

    def put(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        serializer = AnswerUpdateSerializer(answer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        answer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
