# Core
from functools import partial

# Libs
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

# Apps
from apps.posts.services import comment as sv
from apps.posts.serializers import comment as srz
from apps.posts.services.publication import get_publication

# Global
from common.api import empty_response_spec
from common.decorators import permission_required

_comment_api_schema = partial(extend_schema, tags=["💬 Comments"])
_comment_params = OpenApiParameter(
    name="comment_id",
    description="Comment ID.",
    location=OpenApiParameter.PATH,
)


# noinspection PyUnusedLocal
@_comment_api_schema(
    summary="List comments",
    parameters=[
        OpenApiParameter(
            name="code",
            description="Publication code.",
            location=OpenApiParameter.PATH,
        )
    ],
    responses=OpenApiResponse(
        response=srz.CommentInfoSerializer(many=True),
        description="Comments successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("posts.list_comment")
def list_comments(request, code: str) -> Response:
    """Return a comments' information."""

    publication = get_publication(code)
    output = srz.CommentInfoSerializer(
        sv.list_comments(publication),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_comment_api_schema(
    summary="Add comment",
    request=srz.AddCommentSerializer,
    responses=OpenApiResponse(
        response=srz.CommentInfoSerializer,
        description="Comment has been added.",
    ),
)
@api_view(["POST"])
@permission_required("posts.create_comment")
def add_comment(request) -> Response:
    """Comment a publication."""

    payload = srz.AddCommentSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    data["user"] = request.user
    comment = sv.add_comment(fields=data)
    output = srz.CommentInfoSerializer(comment)
    return Response(data=output.data, status=HTTP_201_CREATED)


# noinspection PyUnusedLocal
@_comment_api_schema(
    summary="Remove comment",
    parameters=[_comment_params],
    responses=empty_response_spec("Comment has been removed."),
)
@api_view(["DELETE"])
@permission_required("posts.change_comment")
def remove_comment(request, comment_id: int) -> Response:
    """Remove a comment from a publication."""

    comment = sv.get_comment(comment_id)
    sv.remove_comment(comment=comment)
    return Response(status=HTTP_200_OK)
