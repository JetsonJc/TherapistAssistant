from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
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
            path = request.GET["path"]
            document = get_document(path)
            return Response({"file":document})
        except Exception as err:
            return Response(data=err.args, status=status.HTTP_400_BAD_REQUEST)