import unittest
from src.user import User
from src.product import Product
from src.ecommerce import Ecommerce
from src.state import State
from src.store import Store
from src.shopping_basket import ShoppingBasket
from src.shopping_cart import ShoppingCart
from src.discount_service import DiscountService
from src.buying_policy_service import BuyingPolicyService
from src.delivery_system import DeliveryAddress


class UserTest(unittest.TestCase):
    
    def setUp(self):
        User.num_of_users = 0
        Ecommerce.get_instance().subscribers = []
        Ecommerce.get_instance().stores = []
        Ecommerce.get_instance().complaints = []

    def test_check_details(self): #ok
        self.assertFalse(User.check_details("amir", "123 23"), "space in password")
        self.assertFalse(User.check_details("ofek ash", "123239696"), "space in username")
        self.assertTrue(User.check_details("guygosha", "123456789"), "details are correct")

    def test_search_product(self): #ok
        store1 = Store("ramiLevi", 0, "123123", None, None)
        store1.store_number = 0
        product1 = Product('Apple', 'Fruits', ['Food', 'Fruit', 'Apple'], 5)
        product1.catalog_number = 0
        store1.add_new_product(product1)
        Ecommerce.get_instance().stores = [store1]
        self.assertEqual(len(User.search_product("name", "Apple").val), 1, 'bad')

    def test_add_to_cart(self):#ok
        user1 = User("amir", 12)
        product1 = Product('chocholate', 'Food', ['Food', 'Sweet'], 10)
        product1.catalog_number = 1
        store1 = Store("ramiLevi", 0, "123123", None, None)
        store1.add_new_product(product1)
        Ecommerce.get_instance().stores = [store1]
        store1.inc_product_amount(1, 5)
        self.assertTrue(user1.add_to_cart(1).val, "need return True")
        self.assertFalse(user1.add_to_cart(9).val, "need return False")

    def test_remove_from_cart(self):#ok
        user1 = User("amir", 32)
        user1.identifier = 1
        user1.state = State.STORE_OWNER
        product1 = Product('chocholate', 'Food', ['Food', 'Sweet'], 10)
        product1.catalog_number = 1
        store1 = Store("ramiLevi", 0, "123123", None, None)
        store1.store_number = 0
        store1.supervisor = 1
        store1.add_new_product(product1)
        store1.owners = [user1.identifier]
        Ecommerce.get_instance().stores = [store1]
        self.assertTrue(user1.remove_product(0, 1).val, "need return True")
        self.assertFalse(user1.remove_product(0, 1).val, "need return False")

    def test_login(self): #ok
        user1 = User("amir", 324)
        user1.register("amirdimri", "123456789")
        Ecommerce.get_instance().subscribers = [user1]
        self.assertTrue(user1.login("amirdimri", "123456789").val, "need return True")
        self.assertFalse(user1.login("amirdimri", "123456789").val, "need return False")

    def test_logout(self): #ok
        user1 = User("amir", 123435)
        user1.register("amirdimri", "123456789")
        user1.login("amirdimri", "123456789")
        self.assertTrue(user1.logout().val, "need return True")
        self.assertFalse(user1.logout().val, "need return False")

    def test_open_new_store(self): #ok
        user1 = User("amir", 32)
        user1.register("amirdimri", "123456789")
        user1.login("amirdimri", "123456789")
        user1.state = State.GUEST
        self.assertFalse(user1.open_new_store("akdamon", 123456).val, "need return false")
        user1.state = State.STORE_OWNER
        self.assertTrue(user1.open_new_store("shnizale", 432567).val, "need return True")

    def test_register(self): #ok
        user1 = User("amir", 1)
        user2 = User("roie", 13)
        self.assertTrue(user1.register("amirdimri", "123456789").val, "need return True")
        self.assertFalse(user2.register("roie or","132456789").val, "need return False")
        self.assertFalse(user2.register("roie", "1324").val, "need return False")

    def test_remove_subscriber(self): #ok
        user1 = User("amir", 1)
        user1.identifier = 0
        Ecommerce.get_instance().subscribers = [user1]
        user2 = User("ofek", 13)
        user2.identifier = 1
        user2.state = State.GUEST
        self.assertFalse(user2.remove_subscriber(0).val, "need return False")
        user2.state = State.SYSTEM_ADMINISTRATOR
        self.assertTrue(user2.remove_subscriber(0), "need return False")

    def test_inc_product_amount(self): #ok
        user1 = User("amir", 13)
        user1.identifier = 0
        store1 = Store("ramiLevi", 0, "123123", None, None)
        store1.store_number = 0
        product1 = Product('Banana', 'Fruits', ['Food', 'Fruit', 'Apple'], 5)
        product1.catalog_number = 0
        store1.add_new_product(product1)
        Ecommerce.get_instance().stores = [store1]
        user1.state = State.GUEST
        self.assertFalse(user1.inc_product_amount(0, 0, 3).val, "need return False")
        user1.state = State.STORE_OWNER
        self.assertTrue(user1.inc_product_amount(0, 0, 3).val, "need return True")
        self.assertFalse(user1.inc_product_amount(100, 0, 3).val, "need return False")
        self.assertFalse(user1.inc_product_amount(0, 10, 3).val, "need return False")

    def test_add_new_product(self):#ok
        user1 = User("amir", 2)
        user1.identifier = 0
        store1 = Store("ramiLevi", 0, "123123", None, None)
        store1.supervisor = 1
        Ecommerce.get_instance().stores = [store1]
        user1.state = State.STORE_OWNER
        self.assertTrue(user1.add_new_product(0, "chocholate", 5, "Food", ['Food', 'Sweet']), "need return True")

    def test_remove_product(self): #ok
        user1 = User("amir", 12)
        user1.identifier = 0
        store1 = Store("mega", 0, "456456", None, None)
        store1.store_number = 1
        product1 = Product('chocholate', 'Food', ['Food', 'Sweet'], 10)
        product1.catalog_number = 1
        store1.add_new_product(product1)
        Ecommerce.get_instance().stores = [store1]
        user1.state = State.GUEST
        self.assertFalse(user1.remove_product(1, 1).val, "need return False")
        user1.state = State.STORE_OWNER
        self.assertTrue(user1.remove_product(1, 1), "need return True")
        self.assertFalse(user1.remove_product(1, 10).val, "need return False")

    def test_show_cart(self):
        pass

    def test_change_details_of_product(self):
        user1 = User("amir", 1)
        user1.identifier = 0
        user1.username = "amirdi"
        user1.password = "123456789"
        user1.state = State.STORE_OWNER
        user1.is_logged_in = True

        store1 = Store("mega", 1, "123123", None, None)
        store1.store_number = 1

        product1 = Product('chocholate', 'Food', ['Food', 'Sweet'], 10)
        product1.catalog_number = 1

        store1.owners = [0]
        store1.add_new_product(product1)

        Ecommerce.get_instance().subscribers = [user1]
        Ecommerce.get_instance().stores = [store1]

        self.assertTrue(user1.change_details_of_product(1, "name", "whiteChocholate").val, "need return True")
        self.assertFalse(user1.change_details_of_product(2, "name", "whiteChocholate").val, "need return False")

    def test_add_store_owner(self):
        pass

    def test_add_store_manager(self):
        pass

    def test_remove_store_owner(self):
        pass

    def test_remove_store_manager(self):
        pass

    def test_make_purchase(self):
        user = User('ofek', 18)
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        address = DeliveryAddress(13, 'Israel')
        store = Store('effect', 123, 123, discount_service, buying_policy)
        Ecommerce.get_instance().stores.append(store)
        cart = ShoppingCart(store)
        product = Product('israeli schnitzel', 'schnitzel', ['hot', 'casher'], 15)
        store.products.append({'product': product, 'amount': 5})
        cart.products[product.catalog_number] = {'product': product, 'amount': 4}
        user.shopping_basket.shopping_carts.append(cart)
        all_transactions_been_made = user.make_purchase('paypal', ['ofek', '4580160114431651', '7',
                                                                             '20', '458'], address)
        self.assertEqual(len(all_transactions_been_made), 1)
        self.assertEqual(store.products[0]['amount'], 1)
