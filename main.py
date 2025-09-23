import asyncio
import logging

import uvicorn
from django.conf import settings
from django.core.asgi import get_asgi_application
from telegram import Update

from bot.dispatcher import TELEGRAM_BOT

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

    await TELEGRAM_BOT.bot.delete_webhook(drop_pending_updates=True)
    await TELEGRAM_BOT.bot.set_webhook(
        url=f"{settings.EXTERNAL_URL}bot/update/",
        allowed_updates=Update.ALL_TYPES,
        secret_token=settings.TELEGRAM_SECRET,
    )

    async with TELEGRAM_BOT:
        logger.info(await TELEGRAM_BOT.bot.get_me())
        logger.info(await TELEGRAM_BOT.bot.get_webhook_info())
        try:
            await TELEGRAM_BOT.start()
            await server.serve()
        except Exception as error:
            logger.error("An error occurred: %s", error)
        finally:
            await TELEGRAM_BOT.stop()


if __name__ == "__main__":
    asyncio.run(main())
