from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import TelegramAuthView, TelegramBotWebhookView

app_name = "bot"
urlpatterns = [
    path(
        "update/",
        csrf_exempt(TelegramBotWebhookView.as_view()),
        name="telegram_webhook",
    ),
    path("webapp/", TelegramAuthView.as_view(), name="webapp"),
]
