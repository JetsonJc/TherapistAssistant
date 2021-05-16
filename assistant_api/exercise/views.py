from django.db import transaction
from django.http import Http404
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from data.models import Exercise
from .serializers import *
from utility.pagination import (
    PaginationHandlerMixin,
    Paginator,
)
from utility.serializers import PaginatorSerializer
from utility.storage import (
    post_document,
    delete_document,
)
from utility.constant import PATH_EXERCISES

class ExerciseList(APIView, PaginationHandlerMixin):
    def _get_last_id(self):
        try:
            exercise = Exercise.objects.latest('id')
            return (exercise.id + 1)
        except Exercise.DoesNotExist:
            return 1
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
        try:
            serializer = ExerciseRequestSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    exercise_id = self._get_last_id()
                    video = request.FILES['video']
                    document = request.FILES['document']
                    request.data["path_video"] = post_document(f'{PATH_EXERCISES}{str(exercise_id)}/video', video)
                    request.data["id"] = exercise_id
                    request.data["path_points"] = post_document(f'{PATH_EXERCISES}{str(exercise_id)}/points', document)
                    serializer = ExerciseListSerializer(data=request.data)
                    if serializer.is_valid():
                        exercise = serializer.save()
                        exercise_id = exercise.id
                        return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            raise ValidationError(err.args)


class ExerciseDetail(APIView):
    """
    Retrieve, update or delete a exercise instance.
    """
    def get_object(self, exercise_id):
        try:
            return Exercise.objects.get(pk=exercise_id)
        except Exercise.DoesNotExist:
            raise ValidationError("The requested exercise does not exist.")

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
        request_body=ExerciseRequestUpdateSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def patch(self, request, exercise_id, format=None):
        try:
            serializer = ExerciseRequestUpdateSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    exercise = self.get_object(exercise_id)
                    if 'video' in request.FILES:
                        video = request.FILES['video']
                        delete_document(exercise.path_video)
                        request.data["path_video"] = post_document(f'{PATH_EXERCISES}{str(exercise_id)}/video', video)
                    if 'document' in request.FILES:
                        document = request.FILES['document']
                        delete_document(exercise.path_points)
                        request.data["path_points"] = post_document(f'{PATH_EXERCISES}{str(exercise_id)}/points', document)
                    serializer = ExerciseUpdateSerializer(exercise, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            raise ValidationError(err.args)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def delete(self, request, exercise_id, format=None):
        try:
            with transaction.atomic():
                exercise = self.get_object(exercise_id)
                delete_document(exercise.path_video)
                delete_document(exercise.path_points)
                exercise.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            raise ValidationError(err.args)