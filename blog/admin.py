from django.contrib import admin
from blog.models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'published', 'number_views')
    search_fields = ('title', 'content')
    list_filter = ('published', 'created_at')
