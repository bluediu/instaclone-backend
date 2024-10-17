from django.core.validators import FileExtensionValidator
from rest_framework import serializers as srz

from common.serializers import Serializer
from constants import IMAGE_EXTENSION


class UserInfoSerializer(Serializer):
    """A user info output serializer."""

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
    email = srz.EmailField(
        help_text="E-mail address.",
        required=False,
    )
    avatar = srz.URLField(
        help_text="Avatar URL.",
        required=False,
    )
    description = srz.CharField(
        help_text="Description.",
        required=False,
    )
    website = srz.URLField(
        help_text="Website URL.",
        required=False,
    )
    is_active = srz.BooleanField(help_text="Is the user active?.")
    is_staff = srz.BooleanField(help_text="Is the user staff?.")
    date_joined = srz.DateTimeField(help_text="Created at time.")
    updated_at = srz.DateTimeField(help_text="Updated at time.")


class UserSearchInfoSerializer(Serializer):
    """A user search info output serializer."""

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


class AuthUserInfoSerializer(Serializer):
    """An auth user info output serializer."""

    refresh = srz.CharField(help_text="Refresh token.")
    access = srz.CharField(help_text="Access token.")
    user_id = srz.IntegerField(help_text="User ID.")
    username = srz.CharField(help_text="Username.")
    first_name = srz.CharField(
        help_text="First name.",
        required=False,
    )
    last_name = srz.CharField(
        help_text="Last name.",
        required=False,
    )
    email = srz.EmailField(
        help_text="E-mail address.",
        required=False,
    )


class UserCreateSerializer(Serializer):
    """A user create input serializer."""

    username = srz.CharField(
        help_text="Username.",
        max_length=150,
    )
    password = srz.CharField(
        help_text=(
            "<b>Password requirement:</b> <br>"
            "<ul>"
            "<li>Your password can’t be too similar to your other personal "
            "information.</li>"
            "<li>Your password must contain at least 8 characters.</li>"
            "<li>Your password can’t be a commonly used password.</li>"
            "<li>Your password can’t be entirely numeric.</li>"
            "</ul>"
        ),
        max_length=128,
        min_length=8,
    )
    repeat_password = srz.CharField(
        help_text="Repeat password.",
        max_length=128,
        min_length=8,
    )
    first_name = srz.CharField(
        help_text="First names (optional).",
        max_length=100,
        allow_blank=True,
        required=False,
    )
    last_name = srz.CharField(
        help_text="Last names (optional).",
        max_length=100,
        allow_blank=True,
        required=False,
    )
    email = srz.EmailField(
        help_text="Contact e-mail.",
        max_length=100,
    )
    description = srz.CharField(
        help_text="Description (optional).",
        required=False,
        allow_blank=True,
    )
    website = srz.URLField(
        help_text="Website (optional).",
        required=False,
        allow_blank=True,
    )

    @staticmethod
    def validate_password(password: str) -> str:
        """Validate that password is not entirely numeric."""
        if password.isdigit():
            raise srz.ValidationError("Your password cannot be entirely numeric.")
        return password


class UserUpdateSerializer(UserCreateSerializer):
    """A user update input serializer."""

    password = None
    repeat_password = None
    email = None

    def __init__(self, *args, **kwargs):
        """Override default initialization."""
        super().__init__(*args, **kwargs)
        self.fields["username"].required = False
        self.fields["username"].required = False


class UserAvatarSerializer(Serializer):
    """A user avatar input serializer."""

    avatar = srz.ImageField(
        help_text="Avatar image.",
        validators=[
            FileExtensionValidator(IMAGE_EXTENSION),
        ],
    )
