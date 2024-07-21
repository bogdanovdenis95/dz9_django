# catalog/tests.py

from django.test import TestCase
from unittest.mock import patch
from catalog.services import get_categories
from catalog.models import Category

class CategoryServiceTests(TestCase):

    @patch('catalog.services.cache.get')
    @patch('catalog.services.cache.set')
    @patch('catalog.services.Category.objects.all')
    def test_get_categories_cache_hit(self, mock_get_all, mock_set, mock_get):
        mock_get.return_value = ['category1', 'category2']
        result = get_categories()
        self.assertEqual(result, ['category1', 'category2'])
        mock_get.assert_called_once_with('categories_list')
        mock_set.assert_not_called()

    @patch('catalog.services.cache.get')
    @patch('catalog.services.cache.set')
    @patch('catalog.services.Category.objects.all')
    def test_get_categories_cache_miss(self, mock_get_all, mock_set, mock_get):
        mock_get.return_value = None
        mock_get_all.return_value = ['category1', 'category2']
        result = get_categories()
        self.assertEqual(result, ['category1', 'category2'])
        mock_get.assert_called_once_with('categories_list')
        mock_set.assert_called_once_with('categories_list', ['category1', 'category2'], timeout=900)
