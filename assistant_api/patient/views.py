from datetime import date
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from data.models import (
    ResultExercise,
    PatientRoutine,
)
from .serializers import *
from utility.pagination import (
    PaginationHandlerMixin,
    Paginator,
)
from utility.serializers import PaginatorSerializer
from utility.storage import post_document
from utility.constant import PATH_PATIENT_RESULTS


@method_decorator(
    name='get', decorator=swagger_auto_schema(
        query_serializer=PaginatorSerializer,
        responses={
            status.HTTP_200_OK: PatientResultsDocSerializer,
            status.HTTP_400_BAD_REQUEST: "Retorna un mensaje de error si hubo un problema."
        }
    )
)
class PatientResultsList(ListAPIView, PaginationHandlerMixin):
    serializer_class = PatientResultsListSerializer
    pagination_class = Paginator
    def get_queryset(self):
        exercise = self.kwargs['exercise_id']
        patient_routine = self.kwargs['patient_routine_id']
        return ResultExercise.objects.filter(patient_routine_id=patient_routine, exercise_id=exercise)


class PatientResultsCreate(APIView):
    def _get_object(self, id):
        try:
            return PatientRoutine.objects.get(pk=id)
        except ResultExercise.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        request_body=PatientResultsInsertRequestSerializer,
        responses={
            status.HTTP_201_CREATED: 'If the request was successful, nothing is returned.'
        }
    )
    def post(self, request, format=None):
        try:
            serializer = PatientResultsInsertRequestSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    patient = self._get_object(request.data["patient_routine"])
                    full_date = date.today().strftime("%d%m%Y")
                    video = request.FILES['video']
                    points = request.FILES['points']
                    feedback = request.FILES['feedback']
                    request.data["path_video"] = post_document(f'{PATH_PATIENT_RESULTS}{str(patient.id)}/{full_date}/video', video)
                    request.data["path_points"] = post_document(f'{PATH_PATIENT_RESULTS}{str(patient.id)}/{full_date}/points', points)
                    request.data["path_feedback"] = post_document(f'{PATH_PATIENT_RESULTS}{str(patient.id)}/{full_date}/feedback', feedback)
                    serializer = PatientResultsInsertSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            raise ValidationError(err.args)


class PatientResultsDetail(APIView):
    """
    Retrieve, update or delete records that relate results and patients instance.
    """
    def get_object(self, result_exercise_id):
        try:
            return ResultExercise.objects.get(pk=result_exercise_id)
        except ResultExercise.DoesNotExist:
            raise Http404


    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: PatientResultsListSerializer
        }
    )
    def get(self, request, result_exercise_id, format=None):
        routines = self.get_object(result_exercise_id)
        serializer = PatientResultsListSerializer(routines)
        return Response(serializer.data)


    @swagger_auto_schema(
        request_body=PatientResultsUpdateSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def patch(self, request, result_exercise_id, format=None):
        patient_routines = self.get_object(result_exercise_id)
        serializer = PatientResultsUpdateSerializer(patient_routines, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def delete(self, request, result_exercise_id, format=None):
        patient_results = self.get_object(result_exercise_id)
        patient_results.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(
    name='get', decorator=swagger_auto_schema(
        query_serializer=PaginatorSerializer,
        responses={
            status.HTTP_200_OK: PatientCompleteRoutinesDocSerializer,
            status.HTTP_400_BAD_REQUEST: "Retorna un mensaje de error si hubo un problema."
        }
    )
)
class PatientCompleteRoutinesList(ListAPIView, PaginationHandlerMixin):
    serializer_class = PatientCompleteRoutinesListSerializer
    pagination_class = Paginator
    def get_queryset(self):
        patient = self.kwargs['patient_id']
        return PatientRoutine.objects.filter(patient = patient)


class PatientRoutinesList(APIView, PaginationHandlerMixin):
    pagination_class = Paginator
    """
    List all snippets, or create a new record that relates routines and patients.
    """
    @swagger_auto_schema(
        query_serializer=PaginatorSerializer,
        responses={
            status.HTTP_200_OK: PatientRoutinesDocSerializer
        }
    )
    def get(self, request, patient_id, format=None):
        patient = PatientRoutine.objects.filter(patient = patient_id)
        page = self.paginate_queryset(patient)
        if page is not None:
            serializer = self.get_paginated_response(PatientRoutinesListSerializer(page, many=True).data)
        else:
            serializer = PatientRoutinesListSerializer(patient, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PatientRoutinesUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: 'If the request was successful, nothing is returned.'
        }
    )
    def post(self, request, patient_id, format=None):
        request.data['patient'] = patient_id
        serializer = PatientRoutinesInsertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientRoutineDetail(APIView):
    """
    Retrieve, update or delete records that relate routines and patients instance.
    """

    def get_object(self, patient_id, routine_id):
        try:
            patients = PatientRoutine.objects.filter(patient=patient_id, routine=routine_id).first()
            if patients:
                return patients
            else:
                raise Http404
        except PatientRoutine.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: PatientRoutinesListSerializer
        }
    )
    def get(self, request, patient_id, routine_id, format=None):
        routines = self.get_object(patient_id, routine_id)
        serializer = PatientRoutinesListSerializer(routines)
        return Response(serializer.data)


    @swagger_auto_schema(
        request_body=PatientRoutinesUpdateSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def patch(self, request, patient_id, routine_id, format=None):
        patient_routines = self.get_object(patient_id, routine_id)
        serializer = PatientRoutinesUpdateSerializer(patient_routines, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: 'If the request was successful, nothing is returned.'
        }
    )
    def delete(self, request,  patient_id, routine_id, format=None):
        patient_routines = self.get_object(patient_id, routine_id)
        patient_routines.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

