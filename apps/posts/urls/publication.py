# Libs
from django.urls import include, path

# Apps
import apps.posts.apis.publication as api

publications_patterns = [
    path("create/", api.create_publication, name="create"),
    path(
        "<str:code>/",
        include(
            [
                path("get/", api.get_publication, name="get"),
                path("update/", api.update_publication, name="update"),
                path("delete/", api.delete_publication, name="delete"),
            ]
        ),
    ),
    path(
        "<str:username>/",
        include(
            [
                path("list/", api.list_publications, name="list"),
            ]
        ),
    ),
]
