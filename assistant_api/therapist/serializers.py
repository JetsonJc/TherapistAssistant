from rest_framework import serializers
from data.models import (
    User,
    Exercise,
)

__all__ = (
    'PatientListSerializer',
)

class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'user_type','therapist')
