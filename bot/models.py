from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        help_text="Telegram user ID",
    )
    telegram_username = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Telegram username (without @)",
    )
    telegram_first_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Telegram first name",
    )
    telegram_last_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Telegram last name",
    )

    def __str__(self):
        return self.username or str(self.user_id)
