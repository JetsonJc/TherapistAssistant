from django.db.models import fields
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
    'PatientResultsInsertRequestSerializer',
    'PatientResultsRequestUpdateSerializer',
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


class PatientResultsInsertRequestSerializer(serializers.ModelSerializer):
    video = serializers.FileField(help_text="Video del ejercicio.")
    points =  serializers.FileField(help_text="Points(JSON) del ejercicio.")
    feedback =  serializers.FileField(help_text="Feedback(JSON) del ejercicio.")
    class Meta:
        model = ResultExercise
        exclude = ('id', 'created_at', 'path_video', 'path_points', 'path_feedback')


class PatientResultsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultExercise
        fields = ('path_video', 'path_points', 'path_feedback')


class PatientResultsRequestUpdateSerializer(serializers.Serializer):
    video = serializers.FileField(required=False, help_text="Video del ejercicio.")
    points =  serializers.FileField(required=False, help_text="Points(JSON) del ejercicio.")
    feedback =  serializers.FileField(required=False, help_text="Feedback(JSON) del ejercicio.")


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