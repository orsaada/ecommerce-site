import unittest
from src.transaction_management import TransactionManagement
from src.delivery_system import DeliverySystem
from src.shopping_cart import ShoppingCart
from src.payments_system import PaymentsSystem
from src.delivery_system import DeliveryAddress
from src.discount_service import DiscountService
from src.store import Store
from src.buying_policy_service import BuyingPolicyService
from src.product import Product


class TransactionManagementTest(unittest.TestCase):

    transaction_management = TransactionManagement(PaymentsSystem(), DeliverySystem())

    def setUp(self):
        self.transaction_management.transactions = []

    def test_execute_transaction(self):
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store = Store('effect', 123, 123, discount_service, buying_policy)
        cart = ShoppingCart(store)
        product_a = Product('france schnitzel', 'schnitzel', ['hot', 'krispy'], 35)
        cart.add_product(product_a)
        delivery_address = DeliveryAddress(123, 'Israel')
        store.add_new_product(product_a)
        store.inc_product_amount(product_a.catalog_number, 5)
        trans = (self.transaction_management.execute_transaction(123, cart, 'paypal', ['ofek', '4580160114431651', '7',
                                                                             '20', '458'], delivery_address, 123)).val
        self.assertEqual(trans.total_price, 35)
        self.assertEqual(trans.buyer_identifier, 123)
        self.assertEqual(trans.products[product_a.catalog_number]['product'], product_a)
        self.assertEqual(trans.store_number, store.store_number)
        self.assertEqual(trans.store_account, store.account_number)
        self.assertEqual(len(self.transaction_management.get_transactions()), 1)
        product_b = Product('israeli schnitzel', 'schnitzel', ['hot', 'casher'], 15)
        store.add_new_product(product_b)
        store.inc_product_amount(product_b.catalog_number, 5)
        cart.add_product(product_b)
        trans = (self.transaction_management.execute_transaction(12, cart, 'paypal', ['ofek', '4580160114431651', '7',
                                                                             '20', '458'], delivery_address, 123)).val
        self.assertEqual(trans.total_price, 50)
        self.assertEqual(trans.buyer_identifier, 12)
        self.assertEqual(trans.products[product_a.catalog_number]['product'], product_a)
        self.assertEqual(trans.products[product_b.catalog_number]['product'], product_b)
        self.assertEqual(trans.store_number, store.store_number)
        self.assertEqual(trans.store_account, store.account_number)
        self.assertEqual(len(self.transaction_management.get_transactions()), 2)

    def test_get_transactions_by_store(self):
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store_a = Store('effect', 123, 123, discount_service, buying_policy)
        store_b = Store('effect', 123, 123, discount_service, buying_policy)
        cart = ShoppingCart(store_a)
        product_a = Product('france schnitzel', 'schnitzel', ['hot', 'krispy'], 35)
        store_a.add_new_product(product_a)
        store_a.inc_product_amount(product_a.catalog_number, 5)
        cart.add_product(product_a)
        delivery_address = DeliveryAddress(123, 'Israel')
        trans = (self.transaction_management.execute_transaction(123, cart, 'paypal', ['ofek', '4580160114431651', '7',
                                                                             '20', '458'], delivery_address, 123)).val
        self.assertEqual(self.transaction_management.get_transactions_by_store(store_a.store_number), [trans])
        self.assertEqual(self.transaction_management.get_transactions_by_store(store_b.store_number), [])

    def test_get_transactions_by_identifier(self):
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store = Store('effect', 123, 123, discount_service, buying_policy)
        cart = ShoppingCart(store)
        product_a = Product('france schnitzel', 'schnitzel', ['hot', 'krispy'], 35)
        store.add_new_product(product_a)
        store.inc_product_amount(product_a.catalog_number, 5)
        cart.add_product(product_a)
        delivery_address = DeliveryAddress(123, 'Israel')
        trans = (self.transaction_management.execute_transaction(123, cart, 'paypal', ['ofek', '4580160114431651', '7',
                                                                             '20', '458'], delivery_address, 123)).val
        self.assertEqual(self.transaction_management.get_transactions_by_identifier(123), [trans])
        self.assertEqual(self.transaction_management.get_transactions_by_store(12), [])


