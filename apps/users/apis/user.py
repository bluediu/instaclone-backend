from typing import TypedDict
from functools import partial

from django.http import QueryDict
from rest_framework.response import Response
from django.core.validators import ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.decorators import api_view, authentication_classes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

from apps.users.services import user as sv
from apps.users.serializers import user as srz
from common.decorators import permission_required


_user_api_schema = partial(extend_schema, tags=["Users"])
_user_id_params = OpenApiParameter(
    name="user_id",
    description="User ID.",
    location=OpenApiParameter.PATH,
    type=int,
)


class _UserSearchT(TypedDict):
    """A user search type."""

    search: str


def process_user_query_params(query_params: QueryDict) -> _UserSearchT:
    """Return serialized and validated order query parameters."""
    params: _UserSearchT = {}

    search = query_params.get("search")
    if search is not None:
        try:
            params["search"] = search
        except ValueError:
            raise ValidationError({"search": "Search param must be provided."})

    return params


# noinspection PyUnusedLocal
@_user_api_schema(
    summary="Get user",
    parameters=[_user_id_params],
    responses=OpenApiResponse(
        response=srz.UserInfoSerializer,
        description="User successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("users.view_user")
def get_user(request, user_id: int) -> Response:
    """Return a user's information."""
    user = sv.get_user(user_id)
    output = srz.UserInfoSerializer(user)
    return Response(data=output.data, status=HTTP_200_OK)


@_user_api_schema(
    summary="Search users",
    parameters=[
        OpenApiParameter("search", description="Search user parameter"),
    ],
    responses=OpenApiResponse(
        response=srz.UserInfoSerializer(many=True),
        description="Users successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("users.list_user")
def search_user(request) -> Response:
    """Search users by a term, matching it with username, firstname, or lastname."""
    params = process_user_query_params(request.query_params)
    users = sv.search_user(search_term=params["search"])
    output = srz.UserInfoSerializer(users, many=True)
    return Response(data=output.data, status=HTTP_200_OK)


@_user_api_schema(
    summary="Create user",
    request=srz.UserCreateSerializer,
    responses=OpenApiResponse(
        response=srz.AuthUserInfoSerializer,
        description="User successfully created.",
    ),
)
@authentication_classes(None)
@api_view(["POST"])
def create_user(request) -> Response:
    """Create a new user"""
    payload = srz.UserCreateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    user = sv.create_user(**data)
    output = srz.AuthUserInfoSerializer(user)
    return Response(data=output.data, status=HTTP_201_CREATED)


@_user_api_schema(
    summary="Update user",
    parameters=[_user_id_params],
    request=srz.UserUpdateSerializer,
    responses=OpenApiResponse(
        response=srz.UserUpdateSerializer,
        description="User successfully updated.",
    ),
)
@api_view(["PUT"])
@permission_required("users.change_user")
def update_user(request, user_id: int) -> Response:
    """
    Update a user's information.

    <b>NOTE:</b>
    <small>
    Only a superuser or the account owner can update this user.
    </small>
    """
    payload = srz.UserUpdateSerializer(data=request.data)
    payload.check_data()
    user = sv.get_user(user_id)
    data = sv.update_user(
        user=user,
        request_user=request.user,
        **payload.validated_data,
    )
    output = srz.UserInfoSerializer(data)
    return Response(data=output.data, status=HTTP_200_OK)
