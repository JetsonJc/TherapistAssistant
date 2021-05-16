from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from utility.storage import post_document, get_document
from .serializers import *

class DocumentDetail(APIView):
    @swagger_auto_schema(
        query_serializer=FileSerializer,
        responses={
            status.HTTP_200_OK: FileResponseSerializer
        }
    )
    def get(self, request, format=None):
        try:
            from wsgiref.util import FileWrapper
            from django.http import HttpResponse
            path = request.GET["path"]
            file_data = get_document(path)

            response = HttpResponse(file_data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="file.pdf"'
            return response
        except Exception as err:
            raise ValidationError(err.args)