from rest_framework import serializers
from data.models import (
    User,
    Exercise,
)

__all__ = (
    'PatientListSerializer',
    'PatientDocSerializer',
)


class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'user_type','therapist')


class PatientDocSerializer(serializers.Serializer):
    total = serializers.IntegerField(help_text="Total records.")
    results = PatientListSerializer()
