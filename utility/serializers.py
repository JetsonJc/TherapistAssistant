from rest_framework import serializers

__all__ = (
    'PaginatorSerializer',
)


class PaginatorSerializer(serializers.Serializer):
    limit = serializers.IntegerField(
        required=False,
        help_text="Number of records that are returned."
    )
    offset = serializers.IntegerField(
        required=False,
        help_text="Index from which records are returned."
    )
    total = serializers.BooleanField(
        required=False,
        help_text="Boolean that indicates if it will bring all the records or those that are indicated"
    )