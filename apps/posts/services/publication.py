# Core
from typing import TypedDict, Required, NotRequired, List

# Libs
import cloudinary.uploader

from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.core.validators import ValidationError

# Apps
from apps.users.models import User
from apps.posts.models import Publication

# Functions
from apps.users.services.follow import following_users_ids

# Global
from common import functions as fn


# ==== Local ====
class _PubContextT(TypedDict):
    """A publication create type."""

    image: Required[str]
    description: NotRequired[str]
    user: Required[User]


def _upload_pub_image(*, image) -> str:
    """Upload image to Cloudinary."""
    secure_url, error = fn.upload_to_cloudinary(file=image, folder="publications")
    if error:
        raise ValidationError({"image": error})

    return secure_url


def _remove_pub_image(image_url: str) -> None:
    """Remove image from Cloudinary."""
    public_id = fn.extract_public_id(image_url)
    with transaction.atomic():
        try:
            cloudinary.uploader.destroy(public_id)
        except Exception as error:
            raise ValidationError({"image": str(error)})


def _validate_pub_context(user: User, pub: Publication) -> None:
    """Validate publication context."""
    if not user.is_active:
        raise ValidationError({"user": "Must be active."})

    can_update = pub.user.id != user.id
    if not user.is_superuser and can_update:
        msg = "Forbidden action. Only the account owner can update this publication."
        raise ValidationError(msg)


# ==== Services ====
def get_publications_feed(user: User) -> QuerySet[Publication]:
    """Retrieve the publication feed for the user."""

    users_ids = following_users_ids(user)
    publications = (
        Publication.objects.filter(user__in=[user.id, *users_ids])
        .select_related("user")
        .order_by("-created_at")
    )

    return publications


def get_publication(code: str) -> Publication:
    """Return a publication."""
    return get_object_or_404(Publication, pk=code)


def list_publications(username: str) -> List[Publication]:
    """Return a list of publications."""
    pubs = (
        Publication.objects.filter(user__username=username)
        .select_related("user")
        .order_by("-created_at")
    )

    return pubs


def create_publication(*, request_user: User, fields: _PubContextT) -> Publication:
    """Create a publication."""
    user = fields["user"]

    can_create = user.id != request_user.id
    if not user.is_superuser and can_create:
        msg = "Forbidden action. User inconsistency."
        raise ValidationError(msg)

    # Constrains
    if not user.is_active:
        raise ValidationError({"user": "Must be active."})

    with transaction.atomic():
        # Create preliminar instance.
        publication = Publication(
            code=fn.generate_random_code(),
            description=fields.get("description", ""),
            user=user,
            image="",
        )

        # Upload image to Cloudinary.
        secure_url, error = fn.upload_to_cloudinary(
            file=fields["image"],
            folder="publications",
        )

        if error:
            raise ValidationError({"image": error})

        publication.image = secure_url
        publication.full_clean()
        publication.save(user.id)

    return publication


def update_publication(
    *,
    publication: Publication,
    request_user: User,
    fields: _PubContextT,
) -> Publication:
    """Update a publication."""
    existing_image = publication.image

    # Validations
    _validate_pub_context(request_user, publication)

    changed_fields = publication.update_fields(**fields)
    if "image" in changed_fields:
        # Remove previous pub. image.
        _remove_pub_image(image_url=existing_image)

        # Upload new.
        new_image = _upload_pub_image(image=fields["image"])
        publication.image = new_image

    publication.full_clean()
    publication.save(request_user.id, update_fields=changed_fields)
    return publication


def delete_publication(*, publication: Publication, request_user: User) -> None:
    """Delete a publication."""
    _validate_pub_context(request_user, publication)

    with transaction.atomic():
        # Remove image from Cloudinary.
        _remove_pub_image(image_url=publication.image)

        # Delete database record.
        publication.delete()
