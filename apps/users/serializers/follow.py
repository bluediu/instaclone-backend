# Libs
from rest_framework import serializers as srz

# Global
from common.serializers import Serializer


class IsFollowingInfoSerializer(Serializer):
    """Is following info output serializer."""

    is_following = srz.BooleanField(
        help_text="Check if one user is following another.",
    )


class FollowerInfoSerializer(Serializer):
    """A follower info output serializer."""

    id = srz.IntegerField(help_text="User ID.")
    username = srz.CharField(help_text="Username.")
    first_name = srz.CharField(
        help_text="First name.",
        required=False,
    )
    last_name = srz.CharField(
        help_text="Last name.",
        required=False,
    )
    avatar = srz.URLField(
        help_text="Avatar URL.",
        required=False,
    )


class FollowCountInfoSerializer(Serializer):
    """A follow count info output serializer."""

    following_count = srz.IntegerField(help_text="Number of followed users.")
    followers_count = srz.IntegerField(help_text="Number of followers.")
