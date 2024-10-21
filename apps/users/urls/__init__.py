# Libs
from django.urls import path, include

# Apps
from apps.users.urls.auth import auth_patterns
from apps.users.urls.user import users_patterns
from apps.users.urls.follow import followers_patterns

app_name = "users"


urlpatterns = [
    path("auth/", include((auth_patterns, app_name), namespace="auth")),
    path("user/", include((users_patterns, app_name), namespace="user")),
    path("follow/", include((followers_patterns, app_name), namespace="follow")),
]
