import unittest
from src.product import Product


class ProductTest(unittest.TestCase):

    def setUp(self):
        self.p1 = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        self.p1.catalog_number = 1

    def test_change_detail(self):
        self.assertFalse(self.p1.change_detail('unknown attribute', 'bla bla'))  # SHOULD FAIL

        self.p1.change_detail('name', 'new schnitzel')
        self.assertEqual(self.p1.name, 'new schnitzel')

        self.p1.change_detail('category', 'new category')
        self.assertEqual(self.p1.category, 'new category')

        self.p1.change_detail('key words', ['key words'])
        self.assertEqual(self.p1.key_words, ['key words'])
