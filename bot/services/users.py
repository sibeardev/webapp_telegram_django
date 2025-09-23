import logging

from asgiref.sync import sync_to_async
from django.db import IntegrityError

from bot.models import User

logger = logging.getLogger(__name__)


@sync_to_async
def get_or_create_user(user_data):
    try:
        user, created = User.objects.get_or_create(
            user_id=user_data.id,
            defaults={
                "telegram_username": user_data.username,
                "telegram_first_name": user_data.first_name,
                "telegram_last_name": user_data.last_name,
                "username": user_data.username or f"tg_{user_data.id}",
            },
        )
        return user, created
    except IntegrityError as e:
        logger.error("Failed to create/get user: %s", e)
        return None, False
