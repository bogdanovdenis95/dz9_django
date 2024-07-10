from django.urls import path
from blog.apps import BlogConfig
from blog.views import ArticleCreateView, ArticleListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('blog/create/', ArticleCreateView.as_view(), name='blog_create'),
    path('blog/', ArticleListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', ArticleDetailView.as_view(), name='blog_detail'),  # Использование slug
    path('blog/<slug:slug>/update/', ArticleUpdateView.as_view(), name='blog_update'),  # Использование slug
    path('blog/<slug:slug>/delete/', ArticleDeleteView.as_view(), name='blog_delete'),  # Использование slug
]
