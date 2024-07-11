from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from catalog.models import NULLABLE

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='страна', **NULLABLE)

    token = models.CharField(max_length=100, verbose_name='токен', **NULLABLE)

    groups = models.ManyToManyField(Group, verbose_name='группы', blank=True, related_name='user_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name='разрешения', blank=True, related_name='user_permissions')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
