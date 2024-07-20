# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts.views import RegisterView  # Импортируйте RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls', namespace='catalog')),  # Основной маршрут для вашего приложения
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Путь для страницы входа
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Путь для выхода
    path('accounts/register/', RegisterView.as_view(), name='register'),  # Путь для регистрации
    path('blog/', include('blog.urls', namespace='blog')),  # Основной маршрут для блога
    path('accounts/', include('accounts.urls', namespace='accounts')),  # Основной маршрут для аккаунтов
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Для обработки медиафайлов
