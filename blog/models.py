from django.db import models
from django.utils import timezone

NULLABLE = {"blank": True, "null": True}


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок", help_text="Введите заголовок статьи")
    slug = models.CharField(max_length=100, verbose_name="slug", help_text="slug", **NULLABLE)
    content = models.TextField(verbose_name="Содержимое статьи", help_text="Введите содержимое статьи")
    preview = models.ImageField(upload_to="article_previews/", verbose_name="Превью", help_text="Загрузите превью статьи", **NULLABLE)
    created_at = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(verbose_name="Признак публикации", help_text="Укажите признак публикации", default=True)
    number_views = models.PositiveIntegerField(verbose_name="Количество просмотров", help_text="Укажите количество просмотров", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
