import asyncio
import json
import logging
import traceback

from django.conf import settings
from django.contrib.auth import login
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from telegram import Update
from telegram.error import TelegramError

from bot.dispatcher import TELEGRAM_BOT
from bot.models import User
from bot.utils import validate_telegram_init_data

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


class TelegramAuthView(View):
    template_name = "index.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        init_data = body.get("initData")
        init_data_unsafe = body.get("initDataUnsafe")

        if not init_data or not init_data_unsafe:
            return JsonResponse({"ok": False, "error": "initData not found"}, status=400)

        if not validate_telegram_init_data(init_data, settings.TELEGRAM_TOKEN):
            return JsonResponse({"ok": False, "error": "Invalid init data"}, status=403)

        user_data = init_data_unsafe.get("user")
        user, _ = User.update_or_create_from_telegram(user_data)

        login(request, user)

        return JsonResponse({"ok": True, "user": user.username})
