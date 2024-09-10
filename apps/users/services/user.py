from django.db import transaction
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.search import SearchVector


from apps.users.models import User

DEFAULT_GROUPS = ["Users", "Posts", "Comments", "Followers"]


def _check_password_match(fields: dict) -> None:
    """Check passwords' integrity."""
    if fields["password"] != fields["repeat_password"]:
        raise ValidationError({"password": "Password does not match"})

    fields.pop("repeat_password")


def get_user(user_id: int) -> User:
    """Return a user."""
    return get_object_or_404(User, id=user_id)


def search_user(*, search_term: str) -> list[User]:
    """Search a user."""
    users = User.objects.annotate(
        search=SearchVector("username", "first_name", "last_name")
    ).filter(search=search_term)

    return users


def create_user(**fields: dict) -> User:
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
    return user


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
