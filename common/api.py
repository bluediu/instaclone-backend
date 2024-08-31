from django.core import exceptions
from django.http import Http404, HttpResponse
from drf_spectacular.utils import OpenApiResponse

from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler


def api_exception_http(exc, context) -> HttpResponse:
    """
    Return a standard exception http response.

    For error responses will return a JSON object with the single
    key `errors` containing relevant information describing the problem.
    """
    if isinstance(exc, exceptions.ValidationError):
        exc = ValidationError(as_serializer_error(exc))
    if isinstance(exc, Http404):
        exc = NotFound(exc)
    if isinstance(exc, exceptions.PermissionDenied):
        exc = PermissionDenied("Insufficient privileges to perform this action.")

    response = exception_handler(exc, context)

    if response:
        response.data = {"errors": response.data}

    return response


def empty_response_spec(description: str) -> OpenApiResponse:
    """Return an API specification empty response."""
    if not description.endswith("."):
        description = f"{description}."
    description = f"{description} No response body."
    return OpenApiResponse(description=description)
