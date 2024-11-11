# Libs
from django.urls import include, path

# Apps
import apps.posts.apis.comment as api

comments_patterns = [
    path("add/", api.add_comment, name="add"),
    path(
        "<str:code>/",
        include([path("list/", api.list_comments, name="list")]),
    ),
    path(
        "<int:comment_id>/",
        include([path("remove/", api.remove_comment, name="remove")]),
    ),
]
