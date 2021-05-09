from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from utility.storage import post_document, get_document

class DocumentDetail(APIView):
    @swagger_auto_schema(
        #request_body='completar',
        responses={
            status.HTTP_200_OK: "response"
        }
    )
    def post(self, request, format=None):
        name = "documents/1/video.mp4"
        from django.http import StreamingHttpResponse
        document = get_document(name)
        return Response(document)