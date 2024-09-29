# Libs
from django.core.validators import FileExtensionValidator

from rest_framework import serializers as srz

# Apps
from apps.users.models import User
from apps.users.serializers.user import UserInfoSerializer

# Global
from constants import IMAGE_EXTENSION
from common.serializers import Serializer


class PublicationInfoSerializer(Serializer):
    """A publication info output serializer."""

    code = srz.CharField(
        help_text="Publication code.",
    )
    image = srz.URLField(
        help_text="Image URL.",
    )
    description = srz.CharField(
        help_text="Description.",
    )
    user = UserInfoSerializer(
        help_text="User information.",
    )
    created_at = srz.DateTimeField(help_text="Created at time.")
    updated_at = srz.DateTimeField(help_text="Updated at time.")


class PublicationCreateSerializer(Serializer):
    """A publication create input serializer."""

    image = srz.ImageField(
        help_text="Publication image.",
        validators=[
            FileExtensionValidator(IMAGE_EXTENSION),
        ],
    )
    description = srz.CharField(
        help_text="Description",
        required=False,
        max_length=100,
    )
    user = srz.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        help_text="User ID",
    )


class PublicationUpdateSerializer(Serializer):
    """A publication update input serializer."""

    image = srz.ImageField(
        help_text="Publication image.",
        validators=[
            FileExtensionValidator(IMAGE_EXTENSION),
        ],
    )
    description = srz.CharField(
        help_text="Description",
        required=True,
        max_length=100,
    )
