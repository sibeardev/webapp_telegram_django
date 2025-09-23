import logging

from telegram import Update, User
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes, filters

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for the /start command.
    """
    user: User = update.effective_user
    await update.message.reply_text(text=user, parse_mode=ParseMode.HTML)


handlers = [CommandHandler("start", start, filters=filters.ChatType.PRIVATE)]
