# Core
from typing import TypedDict, List

# Libs
from django.db.models import QuerySet
from django.core.exceptions import ValidationError

# Apps
from apps.users.models import User, Follow


class IsFollowingT(TypedDict):
    is_following: int


class FollowCountT(TypedDict):
    following_count: int
    followers_count: int


def following_users_ids(user: User) -> List[int]:
    """Following users ids."""

    users_ids = (
        User.objects.filter(followers__follower=user)
        .distinct()
        .values_list("id", flat=True)
    )
    return users_ids


def is_following(*, follower: User, followed: User) -> IsFollowingT:
    """Check if one user is following another."""

    is_following_check = Follow.objects.filter(
        follower=follower,
        followed=followed,
    ).exists()

    return {"is_following": is_following_check}


def add_follow(*, follower: User, followed: User) -> None:
    """Add a follow between a follower and a followed user."""

    # Validations.
    if follower == followed:
        raise ValidationError({"follower": "A user cannot follow himself."})

    data = is_following(followed=followed, follower=follower)
    if data["is_following"]:
        msg = "A user cannot follow the same person more than once."
        raise ValidationError({"followed": msg})

    # Save in DB.
    follow = Follow(follower=follower, followed=followed)
    follow.full_clean()
    follow.save(follower.id)


def unfollow(*, follower: User, followed: User) -> None:
    """Unfollow a user."""
    follow_instance = Follow.objects.filter(follower=follower, followed=followed)

    if not follow_instance.exists():
        msg = "A user cannot unfollow a user they are not following."
        raise ValidationError({"follower": msg})

    follow_instance.delete()


def get_follow_count(*, user: User) -> FollowCountT:
    """Return the count of followers and followed users."""
    counts = {
        "following_count": get_following(user=user).count(),
        "followers_count": get_followers(user=user).count(),
    }

    return counts


def get_following(*, user: User) -> QuerySet[User]:
    """Return a list of users the given user follows."""

    following_users = User.objects.filter(followers__follower=user).distinct()
    return following_users


def get_followers(*, user: User) -> QuerySet[User]:
    """Get the followers of a user."""

    followers = User.objects.filter(following__followed=user)
    return followers


def get_recommended_users(user: User) -> QuerySet[User]:
    """Retrieve the publication feed for the user."""

    users_ids = following_users_ids(user)
    recommended_users = User.objects.exclude(id__in=users_ids).exclude(id=user.id)[:4]
    print(recommended_users)
    return recommended_users
