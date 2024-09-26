# Core
from typing import Any

# Libs
from django.db import models
from django.contrib.auth.models import AbstractUser

# Global
from common.functions import clean_spaces


class User(AbstractUser):
    """A custom user."""

    email = models.EmailField(
        verbose_name="Email address",
        unique=True,
    )
    website = models.URLField(
        verbose_name="Website URL",
        max_length=255,
        blank=True,
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True,
    )
    avatar = models.URLField(
        verbose_name="Avatar",
        max_length=255,
        blank=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Updated at",
        auto_now=True,
    )

    USERNAME_FIELD = "email"
    # removes email from REQUIRED_FIELDS
    REQUIRED_FIELDS = []

    def clean(self):
        """Clean user fields."""
        super().clean()

        self.username = clean_spaces(self.username.lower())
        self.first_name = clean_spaces(self.first_name)
        self.last_name = clean_spaces(self.last_name)
        self.description = clean_spaces(self.description)

    def updated_fields(self, **fields: Any) -> list[str]:
        """Return a list of the changed fields."""
        changed_fields = []
        for field, value in fields.items():
            if getattr(self, field) != value:
                setattr(self, field, value)
                changed_fields.append(field)
        return changed_fields
