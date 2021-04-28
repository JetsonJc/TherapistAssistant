from rest_framework.generics import ListAPIView
from data.models import User
from .serializers import *

class PatientList(ListAPIView):
    serializer_class = PatientListSerializer
    def get_queryset(self):
        therapist = self.kwargs['patient_id']
        return User.objects.filter(therapist=therapist)
