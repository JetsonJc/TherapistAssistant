from rest_framework import serializers
from data.models import (
    User,
    ResultExercise,
)

__all__ = (
    'PatientResultsListSerializer',
)


class PatientResultsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultExercise
        exclude = ('exercise', 'patient_routine')