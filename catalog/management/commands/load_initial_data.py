import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Удаление всех существующих записей
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Загрузка категорий
        with open('fixtures/categories.json', 'r', encoding='utf-8') as file:
            categories_data = json.load(file)
            for category in categories_data:
                Category.objects.create(
                    id=category['pk'],
                    name=category['fields']['name'],
                    description=category['fields']['description']
                )

        # Загрузка продуктов
        with open('fixtures/products.json', 'r', encoding='utf-8') as file:
            products_data = json.load(file)
            for product in products_data:
                Product.objects.create(
                    id=product['pk'],
                    name=product['fields']['name'],
                    description=product['fields']['description'],
                    price=product['fields']['price'],
                    image=product['fields']['image'],
                    manufactured_at=product['fields']['manufactured_at'],
                    category=Category.objects.get(id=product['fields']['category'])
                )