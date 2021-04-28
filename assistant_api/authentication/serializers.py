from rest_framework import serializers
from data.models import User

__all__ = (
    'AuthenticationResponseSerializer',
    'AuthenticationRequestSerializer'
)

class AuthenticationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'created_at', 'therapist')
        depth = 1

class AuthenticationRequestSerializer(serializers.Serializer):
    user = serializers.CharField(help_text="Identifier with which the user logs in.")
    password = serializers.CharField(help_text="User password.")
