from rest_framework import serializers

__all__ = (
    'FileSerializer',
    'FileResponseSerializer',
)

class FileSerializer(serializers.Serializer):
    path = serializers.CharField(help_text="File path.")

class FileResponseSerializer(serializers.Serializer):
    file = serializers.CharField(help_text="File in base64.")