from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from data.models import User
from rest_framework import status
from .serializers import *
from utility.pagination import (
    PaginationHandlerMixin,
    Paginator,
)
from utility.serializers import PaginatorSerializer


@method_decorator(
    name='get', decorator=swagger_auto_schema(
        query_serializer=PaginatorSerializer,
        responses={
            status.HTTP_200_OK: PatientDocSerializer,
            status.HTTP_400_BAD_REQUEST: "Retorna un mensaje de error si hubo un problema."
        }
    )
)
class PatientList(ListAPIView):
    serializer_class = PatientListSerializer
    pagination_class = Paginator
    def get_queryset(self):
        therapist = self.kwargs['patient_id']
        return User.objects.filter(therapist=therapist)
