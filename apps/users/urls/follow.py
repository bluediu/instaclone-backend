# Libs
from django.urls import include, path

# Apps
import apps.users.apis.follow as api

followers_patterns = [
    path("not_following/", api.get_not_following, name="no_following"),
    path(
        "<str:username>/",
        include(
            [
                #  Get
                path("count/", api.get_follow_count, name="count"),
                path("get_followers/", api.get_followers, name="get_followers"),
                path("get_following/", api.get_following, name="get_following"),
                #  Actions
                path("unfollow/", api.unfollow, name="unfollow"),
                path("add_follow/", api.add_follow, name="add_follow"),
                path("is_following/", api.is_following, name="is_following"),
            ]
        ),
    ),
]
