from typing import TypedDict

# Libs
from django.core.exceptions import ValidationError

# Apps
from apps.users.models import User
from apps.posts.models import Like, Publication


class CountLikes(TypedDict):
    count: int


class Liked(TypedDict):
    liked: bool


def add_like(*, user: User, publication: Publication) -> None:
    """Add a like to a publication."""

    # Check if the user has already liked the publication
    if Like.objects.filter(user=user, publication=publication).exists():
        msg = "User has already like this publication"
        raise ValidationError({"publication": msg})

    # Create and save the new like
    like = Like(user=user, publication=publication)
    like.full_clean()
    like.save(user.id)


def remove_like(*, user: User, publication: Publication) -> None:
    """Remove a like from a publication."""
    like = Like.objects.filter(user=user, publication=publication)

    if not like.exists():
        msg = "User has not like this publication"
        raise ValidationError({"publication": msg})

    like.delete()


def count_likes(publication: Publication) -> CountLikes:
    """Count likes from publication."""
    count = Like.objects.filter(publication=publication).count()
    return {"count": count}


def is_publication_liked(*, user: User, publication: Publication) -> Liked:
    """Check if a user has already liked the publication."""
    liked = Like.objects.filter(user=user, publication=publication).exists()
    return {"liked": liked}
