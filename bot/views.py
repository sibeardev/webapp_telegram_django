import json
import logging
import traceback

from django.http import HttpRequest, JsonResponse
from django.views import View
from telegram import Update

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
        except Exception as error:
            logger.warning(
                "Error processing Telegram webhook:\n%s", traceback.format_exc()
            )
            return JsonResponse({"ok": False, "error": str(error)}, status=500)

        return JsonResponse({"ok": "POST request processed"})

    async def get(self, request: HttpRequest, *args, **kwargs):
        return JsonResponse({"ok": "Get request processed. Nothing done"})
