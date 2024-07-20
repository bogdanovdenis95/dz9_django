# catalog/management/commands/create_moderator_group.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создает группу Moderator с необходимыми правами'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Moderator')
        
        permissions = [
            'off_published',
            'change_description',
            'change_category'
        ]

        for perm in permissions:
            permission = Permission.objects.get(codename=perm, content_type=ContentType.objects.get_for_model(Product))
            group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS('Группа модераторов успешно создана/обновлена ​​с необходимыми разрешениями.'))
