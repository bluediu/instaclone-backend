# Core
from functools import partial

# Libs
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

# Apps
from apps.posts.services.publication import get_publication
from apps.posts.services import like as sv
from apps.posts.serializers import like as srz

# Global
from common.api import empty_response_spec
from common.decorators import permission_required

_like_api_schema = partial(extend_schema, tags=["🩷 Likes"])
_like_params = OpenApiParameter(
    name="code",
    description="Publication code.",
    location=OpenApiParameter.PATH,
)


# noinspection PyUnusedLocal
@_like_api_schema(
    summary="Count likes",
    parameters=[_like_params],
    responses=OpenApiResponse(
        response=srz.CountLikesInfoSerializer,
        description="Count likes per publication retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("posts.list_like")
def count_likes(request, code: str) -> Response:
    """Return publications' likes."""
    publication = get_publication(code)
    output = srz.CountLikesInfoSerializer(sv.count_likes(publication))
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_like_api_schema(
    summary="Is publication <<liked>>",
    parameters=[_like_params],
    responses=OpenApiResponse(
        response=srz.LikedInfoSerializer,
        description="Is publication liked?.",
    ),
)
@api_view(["GET"])
@permission_required("posts.view_like")
def is_liked(request, code: str) -> Response:
    """Check if a user has already liked the publication."""
    publication = get_publication(code)
    output = srz.LikedInfoSerializer(
        sv.is_publication_liked(
            user=request.user,
            publication=publication,
        ),
    )
    return Response(data=output.data, status=HTTP_200_OK)


@_like_api_schema(
    summary="Like publication",
    parameters=[_like_params],
    responses=empty_response_spec("Like has been added."),
)
@api_view(["POST"])
@permission_required("posts.create_like")
def add_like(request, code: str) -> Response:
    """Like a publication."""
    publication = get_publication(code)
    sv.add_like(user=request.user, publication=publication)
    return Response(status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_like_api_schema(
    summary="Remove Like",
    parameters=[_like_params],
    responses=empty_response_spec("Like has been removed."),
)
@api_view(["DELETE"])
@permission_required("posts.change_like")
def remove_like(request, code: str) -> Response:
    """Remove a like from a publication."""
    publication = get_publication(code)
    sv.remove_like(user=request.user, publication=publication)
    return Response(status=HTTP_200_OK)
