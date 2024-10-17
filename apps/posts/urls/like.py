# Libs
from django.urls import include, path

# Apps
import apps.posts.apis.like as api

likes_patterns = [
    path(
        "<str:code>/",
        include(
            [
                path("count/", api.count_likes, name="count"),
                path("liked/", api.is_liked, name="liked"),
                path("add/", api.add_like, name="add"),
                path("remove/", api.remove_like, name="remove"),
            ]
        ),
    ),
]
