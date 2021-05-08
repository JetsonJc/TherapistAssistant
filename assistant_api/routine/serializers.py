from rest_framework import serializers
from data.models import (
    Routine,
    ExerciseRoutine,
)

__all__ = (
    'RoutineListSerializer',
    'RoutineDocSerializer',
    'CompleteRoutineListSerializer',
    'RoutineInsertDocumentationSerializer',
    'ExerciseRoutineInsertSerializer',
    'RoutineInsertSerializer',
    'RoutineUpdateSerializer',
)

class ExerciseRoutineListSerializer(serializers.ModelSerializer):
    ''' Just for swagger '''
    exercise_id = serializers.CharField(source='exercise.id')
    name = serializers.CharField(source='exercise.name')
    descripcion = serializers.CharField(source='exercise.descripcion')
    path_video = serializers.CharField(source='exercise.path_video')
    path_points = serializers.CharField(source='exercise.path_points')
    class Meta:
        model = ExerciseRoutine
        exclude = ('id', 'routine', 'exercise')


class CompleteRoutineListSerializer(serializers.ModelSerializer):
    routine_id = serializers.CharField(source="id")
    exercises = ExerciseRoutineListSerializer(source='exerciseroutine_set',many=True)
    class Meta:
        model = Routine
        exclude = ('id',)


class RoutineListSerializer(serializers.ModelSerializer):
    routine_id = serializers.CharField(source="id")
    class Meta:
        model = Routine
        fields = '__all__'


class RoutineDocSerializer(serializers.Serializer):
    total = serializers.IntegerField(help_text="Total records.")
    results = RoutineListSerializer()


class RoutineInsertDocumentationSerializer(serializers.ModelSerializer):
    exercises = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="list of exercise identifiers"
    )
    class Meta:
        model = Routine
        fields = '__all__'


class RoutineInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = '__all__'


class RoutineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        exclude = ('id', )


class ExerciseRoutineInsertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseRoutine
        fields = '__all__'
