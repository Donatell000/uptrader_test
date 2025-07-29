from django.contrib import admin

from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "menu_name", "slug", "parent")
    list_filter = ("menu_name",)
    search_fields = ("name", "slug")
    ordering = ("menu_name", "id")
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "menu_name", "parent")
        }),
        ("Ссылки", {
            "fields": ("named_url", "custom_url"),
            "description": "Можно указать имя маршрута в urls.py или прямой URL (например, https://site.com/page/)"
        }),
    )
