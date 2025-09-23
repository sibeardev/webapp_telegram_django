import logging

from django.conf import settings
from telegram.ext import Application

from .handlers import start

logger = logging.getLogger(__name__)

TELEGRAM_BOT = (
    Application.builder()
    .token(settings.TELEGRAM_TOKEN)
    .concurrent_updates(True)
    .updater(None)
    .build()
)

TELEGRAM_BOT.add_handlers(handlers=[*start.handlers])
