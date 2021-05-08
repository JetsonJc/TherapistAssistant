from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from utility.storage import post_document

class DocumentDetail(APIView):
    @swagger_auto_schema(
        #request_body='completar',
        responses={
            status.HTTP_200_OK: "response"
        }
    )
    def post(self, request, format=None):
        file_obj = request.FILES['file']
        name = "1/video"
        post_document(name, file_obj)
        return Response(data={"detail":"ok"}, status=status.HTTP_200_OK)