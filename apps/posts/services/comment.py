# Core
from typing import TypedDict

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

# Apps
from apps.users.models import User
from apps.posts.models import Publication, Comment


class TComment(TypedDict):
    """Comment fields."""

    comment: str
    publication: Publication
    user: User


def add_comment(*, fields: TComment) -> Comment:
    """Add a comment to a publication."""

    comment = Comment(**fields)
    comment.full_clean()
    comment.save(user_id=fields["user"].id)

    return comment


def remove_comment(*, comment: Comment) -> None:
    """Remove a comment from a publication."""

    comment = Comment.objects.filter(id=comment.id)

    if not comment.exists():
        msg = "User has not comment this publication"
        raise ValidationError({"publication": msg})

    comment.delete()


def get_comment(comment: int) -> Comment:
    """Return a comment."""

    return get_object_or_404(Comment, pk=comment)


def list_comments(publication: Publication) -> QuerySet[Comment]:
    """Return a list of comments of a publication."""

    comments = (
        Comment.objects.filter(publication=publication)
        .only("id", "created_at", "comment", "user")
        .select_related("user")
    )

    return comments
