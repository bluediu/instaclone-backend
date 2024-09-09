from django.urls import include, path

# Apps urls
from apps.users.urls import urlpatterns as users_api

from apps.api.views import APISchemaView, APISpecsView

app_name = "api"


urlpatterns = [
    path("schema/", APISchemaView.as_view(), name="schema"),
    path("specs/", APISpecsView.as_view(), name="specs"),
    path("users/", include((users_api, app_name), namespace="users")),
]
