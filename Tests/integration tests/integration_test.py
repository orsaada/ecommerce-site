import unittest
from src.ecommerce import Ecommerce
from src.state import State
from src.store import Store
from src.product import Product
from src.delivery_system import DeliveryAddress
from src.discount_service import DiscountService
from src.buying_policy_service import BuyingPolicyService
from src.db.db_functions import *

class IntegrationTest(unittest.TestCase):

    def setUp(self):
        SQL.setTestDb()
        SQLHandler.get_instance().setTestDb()
        emptied = False
        while not emptied:
            emptied = empty_tables().val

    def test_register(self):
        self.assertTrue(Ecommerce.get_instance().register("client1", "123456789", 24).val)
        self.assertTrue(Ecommerce.get_instance().register("client2", "123456789", 24).val)
        self.assertTrue(Ecommerce.get_instance().register("client3", "123456789", 24).val)
        self.assertTrue(Ecommerce.get_instance().register("client4", "123456789", 24).val)
        self.assertFalse(Ecommerce.get_instance().register("client1", "123456789", 24).val)

    def test_close_permanently(self):
        Ecommerce.get_instance().register("client1", "123456789", 24)
        Ecommerce.get_instance().register("admin", "123456789", 24)
        self.assertTrue(Ecommerce.get_instance().make_admin("admin",24))
        store_number = Ecommerce.get_instance().open_new_store("ramiLevi", "amirdimri2", "12344", 0, 15, 14).val
        self.assertTrue(Ecommerce.get_instance().close_permanently("admin",store_number))
        # Ecommerce.get_instance().get_stores_of_user_owner("amirdimri")
        self.assertFalse(Ecommerce.get_instance().close_store("client1", store_number))

    def test_add_product_to_cart(self):

        Ecommerce.get_instance().register("client1", "123456789", 24)
        Ecommerce.get_instance().register("admin", "123456789", 24)
        existing_product = Product('Mexican Schnitzel', 'Schnitzels', ['hot', 'crispy', 'spicy'], 45)
        non_existing_product = Product('African Schnitzel', 'Schnitzels', ['???'], 567)

        Ecommerce.get_instance().subscribers = [user]
        Ecommerce.get_instance().stores = [store]
        store.add_new_product(existing_product)
        store.inc_product_amount(existing_product.catalog_number, 5)

        self.assertTrue(Ecommerce.get_instance().add_to_cart(user.shopping_basket, existing_product.catalog_number).val)
        self.assertFalse((Ecommerce.get_instance().add_to_cart(user.shopping_basket,
                                                               non_existing_product.catalog_number)).val)
        self.assertTrue(user.shopping_basket.shopping_carts[0].products[existing_product.catalog_number]['product'] ==
                        existing_product)

    def test_remove_product_from_cart(self):
        user = User('Shlomo', 18)
        user.state = State.SUBSCRIBER

        store = Store("Fruit Store", 5, 123456, None, None)
        store.store_number = 0

        existing_product = Product('Mexican Schnitzel', 'Schnitzels', ['hot', 'crispy', 'spicy'], 45)
        non_existing_product = Product('African Schnitzel', 'Schnitzels', ['???'], 567)

        Ecommerce.get_instance().subscribers = [user]
        Ecommerce.get_instance().stores = [store]
        store.add_new_product(existing_product)
        store.inc_product_amount(existing_product.catalog_number, 5)
        Ecommerce.get_instance().add_to_cart(user.shopping_basket, existing_product.catalog_number)
        self.assertFalse((Ecommerce.get_instance().remove_from_cart(user.shopping_basket,
                                                                    non_existing_product.catalog_number)).val)
        self.assertTrue(user.shopping_basket.shopping_carts[store.store_number].products[existing_product.catalog_number]['product'] == existing_product)
        self.assertTrue(Ecommerce.get_instance().remove_from_cart(user.shopping_basket, existing_product.catalog_number))
        self.assertTrue(len(user.shopping_basket.shopping_carts[store.store_number].products) == 0)

    def test_add_new_product(self):
        s1 = Store("my store", 0, 123213, None, None)
        s1.store_number = 0
        Ecommerce.get_instance().stores = [s1]
        Ecommerce.get_instance().add_new_product(0, 'france schnitzel', 35, 'schnitzel', ['hot', 'crispy'])
        self.assertEqual(len(s1.products), 1)
        Ecommerce.get_instance().add_new_product(0, 'italian schnitzel', 35, 'hotSchnitzel', [])
        self.assertEqual(len(s1.products), 2)

    def test_add_store_owner(self):
        user_a = User('ofek', 18)
        Ecommerce.get_instance().register(user_a, 'ofekash', 'ofekashash')
        Ecommerce.get_instance().login(user_a.identifier, user_a.username, user_a.password)
        user_b = User('ofek', 18)
        Ecommerce.get_instance().register(user_b, 'ofekash', 'ofekashash')
        Ecommerce.get_instance().login(user_b.identifier, user_b.username, user_b.password)
        Ecommerce.get_instance().open_new_store(user_a.identifier, user_a.username, user_a.password, 'copy media', 333)

        Ecommerce.get_instance().open_new_store(user_a.identifier, user_a.username, user_a.password, 'copy media', 333)

        store = Ecommerce.get_instance().stores[0]
        self.assertTrue(Ecommerce.get_instance().add_store_owner(user_a.identifier, user_a.username, user_a.password,
                                                                 store.store_number, user_b.identifier))
        self.assertEqual(store.owners[1], user_b.identifier)
        self.assertEqual(len(store.owners), 2)
        self.assertEqual(store.appoints_list[0]['appoint'], user_a.identifier)
        self.assertEqual(len(store.appoints_list), 1)
        self.assertEqual(store.appoints_list[0]['appointed'][0], user_b.identifier)
        self.assertEqual(len(store.appoints_list[0]['appointed']), 1)

    def test_add_store_manager(self):
        user_a = User('ofek', 18)
        Ecommerce.get_instance().register(user_a, 'ofekash', 'ofekashash')
        Ecommerce.get_instance().login(user_a.identifier, user_a.username, user_a.password)
        user_b = User('ofek', 18)
        Ecommerce.get_instance().register(user_b, 'ofekash', 'ofekashash')
        Ecommerce.get_instance().login(user_b.identifier, user_b.username, user_b.password)
        Ecommerce.get_instance().open_new_store(user_a.identifier, user_a.username, user_a.password, 'copy media', 333)

        Ecommerce.get_instance().open_new_store(user_a.identifier, user_a.username, user_a.password, 'copy media', 333)

        store = Ecommerce.get_instance().stores[0]
        self.assertTrue(Ecommerce.get_instance().add_store_manager(user_a.identifier, user_a.username, user_a.password,
                                                                   store.store_number, user_b.identifier,[]))
        self.assertEqual(store.managers[0], user_b.identifier)
        self.assertEqual(len(store.owners), 1)
        self.assertEqual(len(store.managers), 1)
        self.assertEqual(store.appoints_list[0]['appoint'], user_a.identifier)
        self.assertEqual(len(store.appoints_list), 1)
        self.assertEqual(store.appoints_list[0]['appointed'][0], user_b.identifier)
        self.assertEqual(len(store.appoints_list[0]['appointed']), 1)

    def test_inc_product_amount(self):
        s1 = Store("my store", 1, 123213, None, None)
        s1.store_number = 0
        Ecommerce.get_instance().stores = [s1]
        Ecommerce.get_instance().add_new_product(0, 'france schnitzel', 35, 'schnitzel', ['hot', 'crispy'])
        Ecommerce.get_instance().inc_product_amount(0, 0, 70)

        for p in s1.products:
            if p['product'].catalog_number == 0:
                self.assertEqual(p['amount'], 70)

    def test_remove_product(self):
        s1 = Store("my store", 0, 123213, None, None)
        s1.store_number = 0
        Ecommerce.get_instance().stores = [s1]
        Ecommerce.get_instance().add_new_product(0, 'france schnitzel', 35, 'schnitzel', ['hot', 'crispy'])
        self.assertEqual(len(s1.products), 1)
        Ecommerce.get_instance().remove_product(0, 0)
        self.assertIsNone(s1.get_product(0))

    def test_remove_store_owner(self):
        Ecommerce.get_instance().remove_store_owner("seller", store_number, "notowneryet")
        Ecommerce.get_instance().open_new_store(user_a.identifier, user_a.username, user_a.password, 'copy media', 333)

        Ecommerce.get_instance().open_new_store(user_a.identifier, user_a.username, user_a.password, 'copy media', 333)

        store = Ecommerce.get_instance().stores[0]
        self.assertFalse(Ecommerce.get_instance().remove_store_manager(user_a.identifier, user_a.username,
                                                                       user_a.password, store.store_number,
                                                                       user_b.identifier).val)
        Ecommerce.get_instance().add_store_owner(user_a.identifier, user_a.username, user_a.password,
                                                 store.store_number, user_b.identifier)
        self.assertTrue(Ecommerce.get_instance().remove_store_owner(user_a.identifier, user_a.username, user_a.password,
                                                                    store.store_number, user_b.identifier))
        self.assertEqual(len(store.owners), 1)
        self.assertEqual(store.appoints_list[0]['appoint'], user_a.identifier)
        self.assertEqual(len(store.appoints_list), 1)
        self.assertEqual(len(store.appoints_list[0]['appointed']), 0)

        store = Ecommerce.get_instance().stores[0]
        self.assertFalse(Ecommerce.get_instance().remove_store_manager(user_a.identifier, user_a.username,
                                                                       user_a.password, store.store_number,
                                                                       user_b.identifier).val)
        Ecommerce.get_instance().add_store_owner(user_a.identifier, user_a.username, user_a.password,
                                                 store.store_number, user_b.identifier)
        self.assertTrue(Ecommerce.get_instance().remove_store_owner(user_a.identifier, user_a.username, user_a.password,
                                                                    store.store_number, user_b.identifier))
        self.assertEqual(len(store.owners), 1)
        self.assertEqual(store.appoints_list[0]['appoint'], user_a.identifier)
        self.assertEqual(len(store.appoints_list), 1)
        self.assertEqual(len(store.appoints_list[0]['appointed']), 0)

    def test_remove_store_manager(self):
        user_a = User('ofek', 18)
        Ecommerce.get_instance().register(user_a, 'ofekash', 'ofekashash')
        Ecommerce.get_instance().login(user_a.identifier, user_a.username, user_a.password)
        user_b = User('ofek', 18)
        Ecommerce.get_instance().register(user_b, 'ofekash', 'ofekashash')
        Ecommerce.get_instance().login(user_b.identifier, user_b.username, user_b.password)
        Ecommerce.get_instance().open_new_store(user_a.identifier, user_a.username, user_a.password, 'copy media', 333)

        Ecommerce.get_instance().open_new_store(user_a.identifier, user_a.username, user_a.password, 'copy media', 333)

        store = Ecommerce.get_instance().stores[0]
        self.assertFalse(Ecommerce.get_instance().remove_store_manager(user_a.identifier, user_a.username,
                                                                       user_a.password,
                                                                       store.store_number, user_b.identifier).val)
        Ecommerce.get_instance().add_store_manager(user_a.identifier, user_a.username, user_a.password,
                                                   store.store_number, user_b.identifier, [])
        self.assertTrue(Ecommerce.get_instance().remove_store_manager(user_a.identifier, user_a.username,
                                                                      user_a.password,
                                                                      store.store_number, user_b.identifier).val)
        self.assertEqual(len(store.owners), 1)
        self.assertEqual(len(store.managers), 0)
        self.assertEqual(store.appoints_list[0]['appoint'], user_a.identifier)
        self.assertEqual(len(store.appoints_list), 1)
        self.assertEqual(len(store.appoints_list[0]['appointed']), 0)

    def test_make_purchase(self):
        Ecommerce.get_instance().register("client1", "123456789", 24)
        Ecommerce.get_instance().register("admin", "123456789", 24)
        self.assertTrue(Ecommerce.get_instance().make_admin("admin",24))
        store_number = Ecommerce.get_instance().open_new_store("ramiLevi", "amirdimri2", "12344", 0, 15, 14).val
        catalog_number = Ecommerce.get_instance().add_new_product("seller", 'chocholate', 10, 13, 'Food',
                                                                  store_number,
                                                 ['food','sweet'], 0, 100, 16).val
        Ecommerce.get_instance().add_to_cart("client", catalog_number, None)
        Ecommerce.get_instance().make_purchase("client", "paypal", "23886", DeliveryAddress(12, "israel",
                                                                                           "ashkelon",
                                                                                           "ben yehuda",
                                                                                            "78899"), 22, None)
