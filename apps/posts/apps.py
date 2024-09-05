from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Posts application config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.posts"
    verbose_name = "Posts"
