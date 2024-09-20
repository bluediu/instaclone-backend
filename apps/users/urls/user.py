from django.urls import include, path

import apps.users.apis.user as api

users_patterns = [
    path("search/", api.search_user, name="search"),
    path("create/", api.create_user, name="create"),
    path(
        "<str:username>/",
        include(
            [
                path("get/", api.get_user, name="get"),
                path("update/", api.update_user, name="update"),
            ]
        ),
    ),
]
