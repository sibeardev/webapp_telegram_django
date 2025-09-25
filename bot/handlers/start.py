import logging
from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, filters

from bot.services.users import get_or_create_user

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user, created = await get_or_create_user(update.effective_user)

    if user:
        text = (
            f"Welcome, {user.username}!"
            if created
            else f"Welcome back, {user.username}!"
        )
    else:
        text = "Error creating your user record."

    url = urljoin(settings.EXTERNAL_URL, reverse("bot:webapp"))
    buttons = [[InlineKeyboardButton("🚀 run WebApp", web_app=WebAppInfo(url))]]

    await update.message.reply_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


handlers = [CommandHandler("start", start, filters=filters.ChatType.PRIVATE)]
