from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

from bot.utils import generate_password


class User(AbstractUser):
    user_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
        help_text="Telegram user ID",
    )
    language_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Language code",
    )
    is_premium = models.BooleanField(
        default=False,
        verbose_name="Premium",
    )
    allows_write_to_pm = models.BooleanField(
        default=False,
        verbose_name="Private messages are allowed",
    )
    photo_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Profile photo URL",
    )

    def __str__(self):
        return self.username or str(self.user_id)

    @classmethod
    def update_or_create_from_telegram(cls, user_init_data: dict):
        defaults = {
            "first_name": user_init_data.get("first_name") or "",
            "last_name": user_init_data.get("last_name") or "",
            "username": user_init_data.get("username") or f"tg_{user_init_data['id']}",
            "language_code": user_init_data.get("language_code", None),
            "is_premium": user_init_data.get("is_premium", False),
            "allows_write_to_pm": user_init_data.get("allows_write_to_pm", False),
            "photo_url": user_init_data.get("photo_url", None),
        }
        user, created = cls.objects.update_or_create(
            user_id=user_init_data["id"], defaults=defaults
        )

        if created:
            user.password = make_password(generate_password())
            user.save(update_fields=["password"])

        return user, created
