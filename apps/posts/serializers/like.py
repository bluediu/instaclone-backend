# Libs
from rest_framework import serializers as srz

# Global
from common.serializers import Serializer


class CountLikesInfoSerializer(Serializer):
    """A count likes info output serializer."""

    count = srz.IntegerField(
        help_text="Number of likes.",
    )


class LikedInfoSerializer(Serializer):
    """A publication info output serializer."""

    liked = srz.BooleanField(
        help_text="Is publication liked?.",
    )
