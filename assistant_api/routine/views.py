from django.db import transaction
from django.core.exceptions import ValidationError
from django.http import Http404
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from data.models import (
    Routine,
    ExerciseRoutine
)
from .serializers import *
from utility.pagination import (
    PaginationHandlerMixin,
    Paginator,
)
from utility.serializers import PaginatorSerializer


class CompleteRoutineList(ListAPIView):
    serializer_class = CompleteRoutineListSerializer
    queryset = Routine.objects.all()


class RoutineList(APIView, PaginationHandlerMixin):
    pagination_class = Paginator
    """
    List all routines, or create a new routine.
    """
    @swagger_auto_schema(
        query_serializer=PaginatorSerializer,
        responses={
            status.HTTP_200_OK: RoutineDocSerializer
        }
    )
    def get(self, request, format=None):
        routines = Routine.objects.all()
        page = self.paginate_queryset(routines)
        if page is not None:
            serializer = self.get_paginated_response(RoutineListSerializer(page, many=True).data)
        else:
            serializer = RoutineListSerializer(exercise, many=True)
        return Response(serializer.data)

    def post_exercise_routines(self, data, format=None):
        serializer = ExerciseRoutineInsertSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValidationError("Error when relating exercise to routine.")

    @swagger_auto_schema(
        request_body=RoutineInsertDocumentationSerializer,
        responses={
            status.HTTP_201_CREATED: 'If the request was successful, nothing is returned.'
        }
    )
    def post(self, request, format=None):
        serializer = RoutineInsertSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                routine = serializer.save()
                for exercise_id in request.data['exercises']:
                    data = {
                    "exercise":exercise_id,
                    "routine":routine.id
                    }
                    self.post_exercise_routines(data)
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoutineDetail(APIView):
    """
    Retrieve, update or delete a routine instance.
    """
    def get_object(self, routine_id):
        try:
            return Routine.objects.get(pk=routine_id)
        except Routine.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CompleteRoutineListSerializer
        }
    )
    def get(self, request, routine_id, format=None):
        routine = self.get_object(routine_id)
        serializer = CompleteRoutineListSerializer(routine)
        return Response(serializer.data)


    def get_exercise_routine(self, routine_id):
        try:
            return ExerciseRoutine.objects.filter(routine=routine_id)
        except ExerciseRoutine.DoesNotExist:
            return false

    def delete_exercise_routine(self, exercise_routine):
        exercise_routine.delete()


    def update_exercise_routine(self, data, routine_id):
        exercises_routine = self.get_exercise_routine(routine_id)
        length = len(data)
        routine_list = RoutineList()
        for exercise_routine in exercises_routine:
            flag = False
            for i in range(length):
                if data[i] == exercise_routine.exercise:
                    del data[i]
                    flag = True
                    break
            if not flag:
                self.delete_exercise_routine(exercise_routine)
        for i in range(length):
            data_exercise_routines = {
                "exercise":data[i],
                "routine":routine_id
            }
            routine_list.post_exercise_routines(data_exercise_routines)


    @swagger_auto_schema(
        request_body=RoutineInsertDocumentationSerializer,
        operation_description='''
            All the ids of the exercises must be sent, since if they do not exist,
            create them, if they do not come in the list and exist,
            delete the records that exist and leave the ones that come and exist.''',
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def patch(self, request, routine_id, format=None):
        routine = self.get_object(routine_id)
        serializer = RoutineUpdateSerializer(routine, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                self.update_exercise_routine(list(request.data['exercises']), routine_id)
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def delete(self, request, routine_id, format=None):
        routine = self.get_object(routine_id)
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)