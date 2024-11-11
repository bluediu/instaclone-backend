# Libs
from rest_framework import serializers as srz

# Apps
from apps.posts.models import Publication

# Global
from common.serializers import Serializer, inline_serializer


class AddCommentSerializer(Serializer):
    """An add comment input serializer."""

    comment = srz.CharField(
        help_text="Comment text.",
        min_length=1,
        max_length=250,
    )
    publication = srz.PrimaryKeyRelatedField(
        queryset=Publication.objects.all(),
        help_text="Publication ID",
    )


class CommentInfoSerializer(Serializer):
    """A comment info output serializer."""

    id = srz.IntegerField(
        help_text="Comment ID",
    )
    created_at = srz.DateTimeField(
        help_text="Created at",
    )
    comment = srz.CharField(
        help_text="Comment text.",
    )
    user = inline_serializer(
        name="_UserSrz",
        fields={
            "id": srz.CharField(),
            "username": srz.CharField(),
            "first_name": srz.CharField(),
            "last_name": srz.CharField(),
            "avatar": srz.CharField(),
        },
    )
