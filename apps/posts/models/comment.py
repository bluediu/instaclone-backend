from django.db import models

from apps.users.models import User
from apps.posts.models import Publication

from common.models import BaseModel
from common.functions import clean_spaces


class Comment(BaseModel):
    """A comment model."""

    comment = models.TextField(
        verbose_name="Comment",
        max_length=250,
    )
    publication = models.ForeignKey(
        Publication,
        related_name="comments",
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.PROTECT,
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        permissions = [
            ("create_comment", "Create comment"),
            ("list_comment", "List comment"),
            ("view_comment", "View comment"),
            ("change_comment", "Change comment"),
        ]

    def clean(self):
        """Clean comment fields."""
        self.comment = clean_spaces(self.comment.capitalize())
