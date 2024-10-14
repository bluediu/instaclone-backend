# Core
from functools import partial

# Libs
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.decorators import api_view

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

# Apps
from apps.posts.services import publication as sv
from apps.posts.serializers import publication as srz

# Global
from common.api import empty_response_spec
from common.decorators import permission_required


_publication_api_schema = partial(extend_schema, tags=["📸 Publications"])
_publication_params = OpenApiParameter(
    name="code",
    description="Publication code.",
    location=OpenApiParameter.PATH,
)


# noinspection PyUnusedLocal
@_publication_api_schema(
    summary="Get publication",
    parameters=[_publication_params],
    responses=OpenApiResponse(
        response=srz.PublicationInfoSerializer,
        description="Publication successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("posts.view_publication")
def get_publication(request, code: str) -> Response:
    """Get a single publication."""
    output = srz.PublicationInfoSerializer(sv.get_publication(code))
    return Response(data=output.data, status=HTTP_200_OK)


# noinspection PyUnusedLocal
@_publication_api_schema(
    summary="List publications",
    parameters=[_publication_params],
    responses=OpenApiResponse(
        response=srz.PublicationInfoSerializer(many=True),
        description="Publications successfully retrieved.",
    ),
)
@api_view(["GET"])
@permission_required("posts.list_publication")
def list_publications(request, username: str) -> Response:
    """Return a publications' information."""
    output = srz.PublicationInfoSerializer(
        sv.list_publications(username),
        many=True,
    )
    return Response(data=output.data, status=HTTP_200_OK)


@_publication_api_schema(
    summary="Create publication",
    request=srz.PublicationCreateSerializer,
    responses=OpenApiResponse(
        response=srz.PublicationInfoSerializer,
        description="Publication successfully created.",
    ),
)
@api_view(["POST"])
@permission_required("posts.create_publication")
def create_publication(request) -> Response:
    """Create a new publication."""
    payload = srz.PublicationCreateSerializer(data=request.data)
    payload.check_data()
    data = payload.validated_data
    publication = sv.create_publication(request_user=request.user, fields=data)
    output = srz.PublicationInfoSerializer(publication)
    return Response(data=output.data, status=HTTP_201_CREATED)


@_publication_api_schema(
    summary="Update publication",
    parameters=[_publication_params],
    request=srz.PublicationUpdateSerializer,
    responses=OpenApiResponse(
        response=srz.PublicationInfoSerializer,
        description="Publication successfully updated.",
    ),
)
@api_view(["PUT"])
@permission_required("posts.change_publication")
def update_publication(request, code: str) -> Response:
    """Update a publication's information."""
    payload = srz.PublicationUpdateSerializer(data=request.data)
    payload.check_data()
    publication = sv.get_publication(code)
    data = sv.update_publication(
        publication=publication,
        request_user=request.user,
        fields=payload.validated_data,
    )
    output = srz.PublicationInfoSerializer(data)
    return Response(data=output.data, status=HTTP_200_OK)


@_publication_api_schema(
    summary="Delete publication",
    parameters=[_publication_params],
    responses=empty_response_spec("Publication successfully deleted."),
)
@api_view(["DELETE"])
@permission_required("posts.change_publication")
def delete_publication(request, code: str) -> Response:
    """Delete a publication."""
    publication = sv.get_publication(code)
    sv.delete_publication(publication=publication, request_user=request.user)
    return Response(status=HTTP_204_NO_CONTENT)
