import unittest
from src.store import Store
from src.product import Product


class StoreTest(unittest.TestCase):

    def setUp(self):
        self.store = Store('schnitzale', 23444, 4, None, None)
        self.store.store_number = 0
        self.productA = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        self.productB = Product('italian schnitzel', 'hotSchnitzel', ['hot', 'sweet'], 35)
        self.productA.catalog_number = 0
        self.productB.catalog_number = 1

    def test_add_new_product(self):
        # add first product
        self.assertTrue(self.store.add_new_product(self.productA))
        self.assertEqual(self.store.get_product(0), self.productA)
        self.assertFalse(self.store.add_new_product(self.productA).val)  # Can't add twice

        # add second product
        self.assertTrue(self.store.add_new_product(self.productB))
        self.assertEqual(self.store.get_product(0), self.productA)
        self.assertEqual(self.store.get_product(1), self.productB)
        self.assertFalse(self.store.add_new_product(self.productB).val)  # Can't add twice

    def test_inc_product_amount(self):
        # no such product
        self.assertFalse(self.store.inc_product_amount(self.productA.catalog_number, 4).val)

        # add product and inc amount to 4
        self.store.add_new_product(self.productA)
        self.assertTrue(self.store.inc_product_amount(self.productA.catalog_number, 4).val)
        self.assertEqual(self.store.products[0]['amount'], 4)

    def test_dec_product_amount(self):
        # no such product
        self.assertFalse(self.store.dec_product_amount(self.productA.catalog_number, 4).val)

        # add product, inc amount to 4 and dec by 1
        self.store.add_new_product(self.productA)
        self.store.inc_product_amount(self.productA.catalog_number, 4)
        self.store.dec_product_amount(self.productA.catalog_number, 1)
        self.assertEqual(self.store.products[0]['amount'], 3)

        # do not allow negative inventory
        self.assertFalse(self.store.dec_product_amount(self.productA.catalog_number, 10).val)

    def test_remove_product(self):
        # no such product
        self.assertFalse(self.store.remove_product(self.productA.catalog_number).val)

        # add product and then remove it
        self.store.add_new_product(self.productA)
        self.assertTrue(self.store.remove_product(self.productA.catalog_number).val)
        self.assertEqual(len(self.store.products), 0)

    def test_search_product(self):
        # no such product
        self.assertFalse(self.store.search_product('name', 'france schnitzel'))

        #  no such attribute
        self.store.add_new_product(self.productA)
        self.assertFalse(self.store.search_product('bla bla', 'france schnitzel'))

        # search by name. 1 product in store
        self.store.add_new_product(self.productA)
        self.assertEqual(self.store.search_product('name', 'france schnitzel'), [self.productA])

        # search by name. 2 products in store
        self.store.add_new_product(self.productA)
        self.store.add_new_product(self.productB)
        self.assertEqual(self.store.search_product('name', 'france schnitzel'), [self.productA])
        self.assertEqual(self.store.search_product('name', 'italian schnitzel'), [self.productB])

        # search by category. 1 product in store
        self.store.remove_product(1)  # remove product B
        self.assertEqual(self.store.search_product('category', 'schnitzel'), [self.productA])

        # search by category. 2 products in store
        self.store.add_new_product(self.productB)
        self.assertEqual(self.store.search_product('category', 'schnitzel'), [self.productA])
        self.assertEqual(self.store.search_product('category', 'hotSchnitzel'), [self.productB])

        # search by key words. 1 product in store
        self.store.remove_product(1)  # remove product B
        self.assertEqual(self.store.search_product('key words', ['hot', 'crispy']), [self.productA])

        # search by key words. 2 products in store - key words not shared by both
        self.store.add_new_product(self.productB)
        self.assertEqual(self.store.search_product('key words', ['crispy']), [self.productA])
        self.assertEqual(self.store.search_product('key words', ['sweet']), [self.productB])

        # search by key words. 2 products in store - key words shared by both
        self.assertEqual(self.store.search_product('key words', ['hot']), [self.productA, self.productB])

    def test_get_product(self):
        # no such product
        self.assertEqual(self.store.get_product(0), None)

        # get productA
        self.store.add_new_product(self.productA)
        self.assertEqual(self.store.get_product(0), self.productA)
