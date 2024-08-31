from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView


class APISchemaView(SpectacularAPIView):
    """API schema view."""


class APISpecsView(SpectacularRedocView):
    """API specifications view."""

    url_name = "api:schema"
