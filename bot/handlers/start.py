import logging

from telegram import Update
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

    await update.message.reply_text(text=text, parse_mode=ParseMode.HTML)


handlers = [CommandHandler("start", start, filters=filters.ChatType.PRIVATE)]
