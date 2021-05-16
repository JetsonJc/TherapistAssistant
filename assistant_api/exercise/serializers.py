from rest_framework import serializers
from data.models import (
    Exercise
)

__all__ = (
    'ExerciseListSerializer',
    'ExerciseDocSerializer',
    'ExerciseUpdateSerializer',
    'ExerciseRequestSerializer',
    'ExerciseRequestUpdateSerializer',
)

class ExerciseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'


class ExerciseRequestSerializer(serializers.ModelSerializer):
    document = serializers.FileField()
    video = serializers.FileField()
    class Meta:
        model = Exercise
        exclude = ('id', 'path_video', 'path_points')


class ExerciseDocSerializer(serializers.Serializer):
    total = serializers.IntegerField(help_text="Total records.")
    results = ExerciseListSerializer()


class ExerciseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        exclude = ('id',)


class ExerciseRequestUpdateSerializer(serializers.ModelSerializer):
    document = serializers.FileField(required=False)
    video = serializers.FileField(required=False)
    name = serializers.CharField(required=False)
    descripcion = serializers.CharField(required=False)
    class Meta:
        model = Exercise
        exclude = ('id', 'path_video', 'path_points')
        