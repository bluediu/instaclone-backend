from django.urls import include, path

# Apps urls
from apps.users.urls import urlpatterns as users_api
from apps.posts.urls.like import likes_patterns as like
from apps.posts.urls.comment import comments_patterns as comment
from apps.posts.urls.publication import publications_patterns as publication

from apps.api.views import APISchemaView, APISpecsView

app_name = "api"

posts_api = [
    path("publication/", include((publication, app_name), namespace="publication")),
    path("comment/", include((comment, app_name), namespace="comment")),
    path("like/", include((like, app_name), namespace="like")),
]


urlpatterns = [
    path("schema/", APISchemaView.as_view(), name="schema"),
    path("specs/", APISpecsView.as_view(), name="specs"),
    path("users/", include((users_api, app_name), namespace="users")),
    path("posts/", include((posts_api, app_name), namespace="posts")),
]
