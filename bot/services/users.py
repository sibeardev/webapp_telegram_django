import logging

from asgiref.sync import sync_to_async
from django.db import IntegrityError

from bot.models import User

logger = logging.getLogger(__name__)


@sync_to_async
def get_or_create_user(user_data):
    try:
        user, created = User.update_or_create_from_telegram(user_data)
        return user, created
    except IntegrityError as e:
        logger.error("Failed to create/get user: %s", e)
        return None, False
