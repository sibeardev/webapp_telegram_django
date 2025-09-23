import logging

from django.conf import settings
from telegram.ext import Application

logger = logging.getLogger(__name__)

TELEGRAM_BOT = (
    Application.builder()
    .token(settings.TELEGRAM_TOKEN)
    .concurrent_updates(True)
    .updater(None)
    .build()
)


def setup_handlers(application: Application):
    from bot.handlers import start

    application.add_handlers(handlers=[*start.handlers])
