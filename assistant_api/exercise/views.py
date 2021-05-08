from django.http import Http404
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from data.models import Exercise
from .serializers import *
from utility.pagination import (
    PaginationHandlerMixin,
    Paginator,
)
from utility.serializers import PaginatorSerializer


class ExerciseList(APIView, PaginationHandlerMixin):
    pagination_class = Paginator
    """
    List all exercises, or create a new exercise.
    """
    @swagger_auto_schema(
        query_serializer=PaginatorSerializer,
        responses={
            status.HTTP_200_OK: ExerciseDocSerializer
        }
    )
    def get(self, request, format=None):
        exercise = Exercise.objects.all()
        page = self.paginate_queryset(exercise)
        if page is not None:
            serializer = self.get_paginated_response(ExerciseListSerializer(page, many=True).data)
        else:
            serializer = ExerciseListSerializer(exercise, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ExerciseListSerializer,
        responses={
            status.HTTP_201_CREATED: 'If the request was successful, nothing is returned.'
        }
    )
    def post(self, request, format=None):
        serializer = ExerciseListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExerciseDetail(APIView):
    """
    Retrieve, update or delete a exercise instance.
    """
    def get_object(self, exercise_id):
        try:
            return Exercise.objects.get(pk=exercise_id)
        except Exercise.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ExerciseListSerializer
        }
    )
    def get(self, request, exercise_id, format=None):
        exercise = self.get_object(exercise_id)
        serializer = ExerciseListSerializer(exercise)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ExerciseUpdateSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def patch(self, request, exercise_id, format=None):
        exercise = self.get_object(exercise_id)
        serializer = ExerciseUpdateSerializer(exercise, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def delete(self, request, exercise_id, format=None):
        exercise = self.get_object(exercise_id)
        exercise.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)