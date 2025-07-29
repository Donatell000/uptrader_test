from django.db import models


class MenuItem(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Название пункта",
        help_text="Отображаемое имя пункта меню"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Слаг",
        help_text="Уникальный slug идентификатор"
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
        verbose_name="Родительский пункт",
        help_text="Если указать — пункт станет дочерним"
    )
    menu_name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="Название меню",
        help_text="Служебное имя меню, например: main_menu"
    )
    named_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Named URL",
        help_text="Имя маршрута в urls.py (если используется)"
    )
    custom_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Пользовательский URL",
        help_text="Прямой URL (например, https://site.com/page/)"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self):
        if self.parent:
            return f"{self.parent} → {self.name}"
        return self.name
