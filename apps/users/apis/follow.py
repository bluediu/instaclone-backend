# Core
from functools import partial

# Libs
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

# Apps
from apps.users.services.user import get_user
from apps.users.services import follow as sv
from apps.users.serializers import follow as srz

# Global
from common.api import empty_response_spec
from common.decorators import permission_required

_follow_api_schema = partial(extend_schema, tags=["🤝 Followers"])
_follow_params = OpenApiParameter(
    name="username",
    description="Username.",
    location=OpenApiParameter.PATH,
)


# noinspection PyUnusedLocal
@_follow_api_schema(
    summary="Is following",
    parameters=[_follow_params],
    responses=OpenApiResponse(
        response=srz.IsFollowingInfoSerializer,
        description="Are you following the user?",
    ),
)
@api_view(["GET"])
@permission_required("users.view_follow")
def is_following(request, username: str) -> Response:
    """Check if one user is following another."""

    followed = get_user(username)
    output = srz.IsFollowingInfoSerializer(
        sv.is_following(
            follower=request.user,
            followed=followed,
        )
    )
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_follow_api_schema(
    summary="Get following",
    responses=OpenApiResponse(
        response=srz.FollowerInfoSerializer(many=True),
        description="Following users successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("users.list_follow")
def get_following(request, username: str) -> Response:
    """Return a list of users the given user follows."""

    user = get_user(username)
    output = srz.FollowerInfoSerializer(
        sv.get_following(user=user),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_follow_api_schema(
    summary="Get followers",
    responses=OpenApiResponse(
        response=srz.FollowerInfoSerializer(many=True),
        description="Followers successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("users.list_follow")
def get_followers(request, username: str) -> Response:
    """Return a list of followers of a user."""

    user = get_user(username)
    output = srz.FollowerInfoSerializer(
        sv.get_followers(user=user),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_follow_api_schema(
    summary="Get follow count",
    parameters=[_follow_params],
    responses=OpenApiResponse(
        response=srz.FollowCountInfoSerializer,
        description="Count data successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("users.list_follow")
def get_follow_count(request, username: str) -> Response:
    """Return the count of followers and followed users."""

    user = get_user(username)
    output = srz.FollowCountInfoSerializer(sv.get_follow_count(user=user))
    return Response(data=output.data, status=HTTP_200_OK)


@_follow_api_schema(
    summary="Add follow",
    parameters=[_follow_params],
    responses=empty_response_spec("User has been followed."),
)
@api_view(["POST"])
@permission_required("users.create_follow")
def add_follow(request, username: str) -> Response:
    """Add a follow between a follower and a followed user."""

    followed = get_user(username)
    sv.add_follow(follower=request.user, followed=followed)
    return Response(status=HTTP_200_OK)


@_follow_api_schema(
    summary="Unfollow",
    parameters=[_follow_params],
    responses=empty_response_spec("User has been 'unfollowed'."),
)
@api_view(["DELETE"])
@permission_required("users.change_follow")
def unfollow(request, username: str) -> Response:
    """Unfollow a user."""

    followed = get_user(username)
    sv.unfollow(follower=request.user, followed=followed)
    return Response(status=HTTP_200_OK)
