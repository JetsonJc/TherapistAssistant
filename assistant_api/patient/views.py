from rest_framework.generics import ListAPIView
from data.models import (
    User,
    ResultExercise,
)
from .serializers import *


class PatientResultsList(ListAPIView):
    serializer_class = PatientResultsListSerializer
    def get_queryset(self):
        exercise = self.kwargs['exercise_id']
        patient_routine = self.kwargs['results_id']
        return ResultExercise.objects.filter(patient_routine_id=patient_routine, exercise_id=exercise)