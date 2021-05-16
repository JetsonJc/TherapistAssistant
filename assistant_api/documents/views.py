import os
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
from utility.storage import get_document
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
            path = request.GET["path"]
            extension = os.path.splitext(path)[1]
            file_data = get_document(path)
            if ".json" == extension:
                response = HttpResponse(file_data, content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="file.json"'
            elif ".pdf" == extension:
                response = HttpResponse(file_data, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="file.pdf"'
            elif ".mp4" == extension:
                response = HttpResponse(file_data, content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="file.mp4"'
                response['Content-Length'] = len(file_data)
            return response
        except Exception as err:
            raise ValidationError(err.args)