from django.contrib.auth.hashers import make_password
from django.http import Http404
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from data.models import User
from .serializers import *
from utility.constant import SECRET_KEY_PASS

class AuthenticationDetail(APIView):
    def get_object(self, email, password):
        try:
            return User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        request_body=AuthenticationRequestSerializer,
        responses={
            status.HTTP_200_OK: AuthenticationResponseSerializer
        }
    )
    def post(self, request, format=None):
        serializer = AuthenticationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = make_password(serializer.data['password'], SECRET_KEY_PASS)
        user = self.get_object(serializer.data['user'], password)
        serializer = AuthenticationResponseSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
