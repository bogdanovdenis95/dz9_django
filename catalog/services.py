from django.core.cache import cache
from .models import Category, Product

def get_categories():
    # Попытка получить список категорий из кеша
    categories = cache.get('categories_list')
    
    if not categories:
        # Если данных нет в кеше, извлекаем из базы данных
        categories = list(Category.objects.all())
        # Сохраняем данные в кеш
        cache.set('categories_list', categories, timeout=60*15)  # Кэшируем на 15 минут

    return categories


def get_products():
    # Попытка получить список продуктов из кеша
    products = cache.get('products_list')
    
    if not products:
        # Если данных нет в кеше, извлекаем из базы данных
        products = list(Product.objects.all())
        # Сохраняем данные в кеш
        cache.set('products_list', products, timeout=60*15)  # Кэшируем на 15 минут

    return products
