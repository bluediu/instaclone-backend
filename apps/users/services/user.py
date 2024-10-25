# Libs
from django.db.models import Q
from django.db import transaction
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password


from rest_framework_simplejwt.tokens import RefreshToken

# Apps
from apps.users.models import User

# Global
import cloudinary.uploader
from common import functions as fn


DEFAULT_GROUPS = ["Users", "Posts", "Comments", "Followers"]


# ==== Local ====
def _check_password_match(fields: dict) -> None:
    """Check passwords' integrity."""
    if fields["password"] != fields["repeat_password"]:
        raise ValidationError({"password": "Password does not match"})

    fields.pop("repeat_password")


# ==== Users ====
def get_user(username: str) -> User:
    """Return a user."""
    return get_object_or_404(User, username=username)


def search_user(*, search_term: str) -> list[User]:
    """Search a user."""
    users = (
        User.objects.filter(
            Q(username__icontains=search_term)
            | Q(first_name__icontains=search_term)
            | Q(last_name__icontains=search_term)
        )
        .filter(is_active=True)
        .only("id", "username", "first_name", "last_name", "avatar")
    )

    return users


def create_user(**fields: dict) -> None:
    """Create a user."""
    _check_password_match(fields)
    # Encrypt password using algorithm `pbkdf2_sha256`.
    fields["password"] = make_password(fields["password"])
    user = User(**fields)
    user.full_clean()

    with transaction.atomic():
        user.save()

        # Add groups
        groups = Group.objects.filter(name__in=DEFAULT_GROUPS)
        user.groups.add(*groups)


def update_user(*, user: User, request_user: User, **fields: dict) -> User:
    """Update a user."""

    # Constrains.
    if not request_user.is_superuser and user != request_user:
        msg = "Forbidden action. Only the account owner can update this user."
        raise ValidationError(msg)

    changed_fields = user.updated_fields(**fields)
    user.full_clean()
    user.save(update_fields=changed_fields + ["updated_at"])
    return user


# ==== Avatar ====
def upload_avatar(*, user: User, file) -> User:
    """Upload user avatar."""
    if user.avatar:
        remove_avatar(user=user)

    with transaction.atomic():
        secure_url, error = fn.upload_to_cloudinary(file=file)

        if error:
            raise ValidationError({"avatar": error})

        # Save changes
        user.avatar = secure_url
        user.full_clean()
        user.save(update_fields=["avatar", "updated_at"])

    return user


def remove_avatar(*, user: User) -> User:
    """Delete user avatar."""

    if not user.avatar:
        raise ValidationError({"avatar": "No avatar to delete"})

    # Extract `public_id`
    public_id = fn.extract_public_id(user.avatar)

    with transaction.atomic():
        try:
            cloudinary.uploader.destroy(public_id)
        except Exception as error:
            raise ValidationError({"avatar": str(error)})

        user.avatar = ""
        user.full_clean()
        user.save(update_fields=["avatar", "updated_at"])

    return user
