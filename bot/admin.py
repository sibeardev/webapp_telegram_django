from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from bot.models import User

admin_title = f"{settings.PROJECT_NAME} admin"

admin.site.site_title = admin_title
admin.site.site_header = admin_title
# admin.site.site_url = getattr(settings, "PROJECT_URL", "/") TODO: add Telegram url


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = [
        "avatar",
        "username",
        "user_id",
        "first_name",
        "is_premium",
        "language_code",
        "is_active",
        "date_joined",
        "last_login",
    ]
    list_filter = ["is_premium", "language_code", "is_active"]
    search_fields = ("username", "user_id", "first_name", "last_name")
    readonly_fields = ("user_id",)

    @admin.display(description="Avatar")
    def avatar(self, obj: User):

        avatar_html = (
            f'<img src="{obj.photo_url}" class="w-10 h-10 rounded-full"/>'
            if obj.photo_url
            else (
                '<div class="relative w-10 h-10 overflow-hidden bg-gray-100 rounded-full dark:bg-gray-600">'
                '<svg class="absolute w-12 h-12 text-gray-400 -left-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path></svg>'
                "</div"
            )
        )
        return format_html(avatar_html)

    # Removes the ability to add new users through the admin area
    def has_add_permission(self, request):
        return False
