from rest_framework import serializers
from data.models import (
    ResultExercise,
    PatientRoutine,
)
from assistant_api.routine.serializers import (
    RoutineListSerializer,
    CompleteRoutineListSerializer,
)
__all__ = (
    'PatientResultsListSerializer',
    'PatientRoutinesListSerializer',
    'PatientCompleteRoutinesListSerializer',
    'PatientRoutinesInsertSerializer',
    'PatientRoutinesUpdateSerializer',
    'PatientResultsInsertSerializer',
    'PatientResultsUpdateSerializer',
    'PatientCompleteRoutinesDocSerializer',
    'PatientResultsDocSerializer',
    'PatientRoutinesDocSerializer',
)


class PatientResultsListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='exercise.name')
    class Meta:
        model = ResultExercise
        exclude = ('exercise', 'patient_routine')


class PatientResultsDocSerializer(serializers.Serializer):
    total = serializers.IntegerField(help_text="Total records.")
    results = PatientResultsListSerializer()


class PatientResultsInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultExercise
        fields = '__all__'


class PatientResultsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultExercise
        exclude = ('id', 'patient_routine', 'exercise')


class PatientRoutinesListSerializer(serializers.ModelSerializer):
    patient_routine_id = serializers.CharField(source="id")
    routine = RoutineListSerializer()
    class Meta:
        model = PatientRoutine
        exclude = ('id', 'patient')


class PatientRoutinesDocSerializer(serializers.Serializer):
    total = serializers.IntegerField(help_text="Total records.")
    results = PatientRoutinesListSerializer()


class PatientRoutinesInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRoutine
        fields = '__all__'


class PatientRoutinesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRoutine
        exclude = ('id', 'patient', 'created_at')


class PatientCompleteRoutinesListSerializer(serializers.ModelSerializer):
    patient_routine_id = serializers.CharField(source="id")
    routine = CompleteRoutineListSerializer()
    class Meta:
        model = PatientRoutine
        exclude = ('id', 'patient')


class PatientCompleteRoutinesDocSerializer(serializers.Serializer):
    total = serializers.IntegerField(help_text="Total records.")
    results = PatientCompleteRoutinesListSerializer()