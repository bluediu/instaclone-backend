from django.urls import include, path

# Apps urls
from apps.users.urls import urlpatterns as users_api

from apps.api.views import APISchemaView, APISpecsView
from drf_spectacular.views import SpectacularAPIView

app_name = "api"


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("specs/", APISpecsView.as_view(), name="specs"),
    path("users/", include((users_api, app_name), namespace="users")),
]
