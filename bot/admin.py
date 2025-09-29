from django.contrib import admin

from bot.models import User
from django.conf import settings

admin_title = f"{settings.PROJECT_NAME} admin"

admin.site.site_title = admin_title
admin.site.site_header = admin_title
# admin.site.site_url = getattr(settings, "PROJECT_URL", "/") TODO: add Telegram url


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    # Removes the ability to add new users through the admin area
    def has_add_permission(self, request):
        return False

