import asyncio
import logging
from urllib.parse import urljoin

import uvicorn
from django.conf import settings
from django.core.asgi import get_asgi_application
from django.urls import reverse
from telegram import Update
from telegram.error import NetworkError, TelegramError

from bot.dispatcher import TELEGRAM_BOT, setup_handlers

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def main() -> None:
    server = uvicorn.Server(
        config=uvicorn.Config(
            app=get_asgi_application(),
            use_colors=settings.DEBUG,
            host="0.0.0.0",
            port=settings.PORT,
        )
    )

    setup_handlers(TELEGRAM_BOT)
    await TELEGRAM_BOT.bot.delete_webhook(drop_pending_updates=True)
    await TELEGRAM_BOT.bot.set_webhook(
        url=urljoin(settings.EXTERNAL_URL, reverse("bot:telegram_webhook")),
        allowed_updates=Update.ALL_TYPES,
        secret_token=settings.TELEGRAM_SECRET,
    )

    async with TELEGRAM_BOT:
        try:
            logger.info(await TELEGRAM_BOT.bot.get_me())
            logger.info(await TELEGRAM_BOT.bot.get_webhook_info())
            await TELEGRAM_BOT.start()
            await server.serve()
        except (NetworkError, TelegramError) as error:
            logger.error("Telegram API error: %s", error, exc_info=True)
        except OSError as error:
            logger.error("Server error (port or config issue): %s", error, exc_info=True)
        except asyncio.CancelledError:
            logger.info("Asyncio task cancelled, shutting down gracefully.")
            raise
        except KeyboardInterrupt:
            logger.info("Server stopped manually.")
        except Exception as error:
            logger.error("Unexpected error: %s", error, exc_info=True)
        finally:
            await TELEGRAM_BOT.stop()


if __name__ == "__main__":
    asyncio.run(main())
