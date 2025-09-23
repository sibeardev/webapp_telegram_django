import asyncio
import json
import logging
import traceback

from django.http import HttpRequest, JsonResponse
from django.views import View
from telegram import Update
from telegram.error import TelegramError

from bot.dispatcher import TELEGRAM_BOT

logger = logging.getLogger(__name__)


class TelegramBotWebhookView(View):
    async def post(self, request: HttpRequest, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
            await TELEGRAM_BOT.update_queue.put(Update.de_json(data, TELEGRAM_BOT.bot))
        except json.JSONDecodeError as error:
            logger.warning("Invalid JSON: %s", error, exc_info=True)
            return JsonResponse({"ok": False, "error": "Invalid JSON"}, status=400)
        except (KeyError, TypeError, ValueError, TelegramError) as error:
            logger.warning("Telegram update parsing error: %s", error, exc_info=True)
            return JsonResponse(
                {"ok": False, "error": "Telegram update invalid"}, status=400
            )
        except asyncio.QueueFull as error:
            logger.error("Update queue is full: %s", error, exc_info=True)
            return JsonResponse({"ok": False, "error": "Queue full"}, status=503)
        except Exception as error:
            logger.error(
                "Unexpected error processing webhook: %s", traceback.format_exc()
            )
            return JsonResponse(
                {"ok": False, "error": "Internal server error"}, status=500
            )

        return JsonResponse({"ok": True})

    async def get(self, request: HttpRequest, *args, **kwargs):
        return JsonResponse({"ok": "Get request processed. Nothing done"})
