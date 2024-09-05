from django.db import models

from apps.users.models import User

from common.models import BaseModel


class Follow(BaseModel):
    """A follow model."""

    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.PROTECT,
        verbose_name="Follower",
        help_text="The user who is following another user.",
    )
    followed = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.PROTECT,
        verbose_name="Followed",
        help_text="The user being followed.",
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Follow"
        verbose_name_plural = "Followers"
        permissions = [
            ("create_follow", "Create follow"),
            ("list_follow", "List follow"),
            ("view_follow", "View follow"),
            ("change_follow", "Change follow"),
        ]
        constraints = [
            # A user cannot follow the same person more than once.
            models.UniqueConstraint(
                fields=["follower", "followed"],
                name="%(app_label)s_%(class)s_unique_follow_check",
            ),
            # A user cannot follow himself.
            models.CheckConstraint(
                check=~models.Q(follower=models.F("followed")),
                name="%(app_label)s_%(class)s_prevent_self_follow_check",
            ),
        ]

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
