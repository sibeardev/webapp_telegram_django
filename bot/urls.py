from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import MainPageView, TelegramAuthView, TelegramBotWebhookView

app_name = "bot"
urlpatterns = [
    path("", MainPageView.as_view(), name="main"),
    path(
        "update/",
        csrf_exempt(TelegramBotWebhookView.as_view()),
        name="telegram_webhook",
    ),
    path("auth/", TelegramAuthView.as_view(), name="auth"),
]
