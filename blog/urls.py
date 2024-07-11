from django.urls import path
from blog.views import (
    ArticleCreateView, ArticleListView, ArticleDetailView, 
    ArticleUpdateView, ArticleDeleteView
)

app_name = 'blog'

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='blog_create'),
    path('', ArticleListView.as_view(), name='blog_list'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='blog_detail'),
    path('<slug:slug>/update/', ArticleUpdateView.as_view(), name='blog_update'),
    path('<slug:slug>/delete/', ArticleDeleteView.as_view(), name='blog_delete'),
]