from django.db import models

from apps.users.models import User

from common.models import BaseModel
from common.functions import clean_spaces


class Publication(BaseModel):
    """A publication model."""

    image = models.URLField(
        verbose_name="Image URL",
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        max_length=100,
    )
    user = models.ForeignKey(
        User,
        related_name="publications",
        on_delete=models.PROTECT,
    )

    class Meta(BaseModel.Meta):
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        permissions = [
            ("create_publication", "Create publication"),
            ("list_publication", "List publication"),
            ("view_publication", "View publication"),
            ("change_publication", "Change publication"),
        ]

    def clean(self):
        """Clean publication fields."""
        self.description = clean_spaces(self.description.capitalize())
