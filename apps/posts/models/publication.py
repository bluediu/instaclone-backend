# Libs
from django.db import models
from django.core.validators import RegexValidator

# Apps
from apps.users.models import User

# Global
from common.models import BaseModel
from common.functions import clean_spaces


CODE_LENGTH = 6


class Publication(BaseModel):
    """A publication model."""

    code = models.CharField(
        primary_key=True,
        unique=True,
        validators=[
            RegexValidator(f"^[0-9A-Za-z]{{{CODE_LENGTH}}}$"),
        ],
        max_length=CODE_LENGTH,
    )
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
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_code_valid",
                check=models.Q(code__regex=f"^[0-9A-Za-z]{{{CODE_LENGTH}}}$"),
                violation_error_message="Invalid code.",
            )
        ]

    def clean(self):
        """Clean publication fields."""
        self.description = clean_spaces(self.description.capitalize())
