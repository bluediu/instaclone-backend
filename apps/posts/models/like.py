# Core
from django.db import models

# Apps
from apps.users.models import User
from apps.posts.models import Publication

# Global
from common.models import BaseModel


class Like(BaseModel):
    """A like model."""

    publication = models.ForeignKey(
        Publication,
        to_field="code",
        related_name="likes",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        permissions = [
            ("create_like", "Create like"),
            ("list_like", "List like"),
            ("view_like", "View like"),
            ("change_like", "Change like"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["publication", "user"],
                name="%(app_label)s_%(class)s_unique_user_publication_like_check",
            )
        ]
