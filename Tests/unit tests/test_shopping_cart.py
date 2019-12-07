import unittest
from src.shopping_cart import ShoppingCart
from src.product import Product
from src.store import Store
from src.discount_service import DiscountService
from src.buying_policy_service import BuyingPolicyService


class TestShoppingCart(unittest.TestCase):

    def setUp(self):
        pass
        # self.ProductHolder = namedtuple('ProductHolder', ['product', 'amount'])
        # self.empty_cart = ShoppingCart(10)
        # self.non_empty_cart = ShoppingCart(20)
        # self.products = []
        # for i in range(5):
        #     self.products.append(Product('Apple', 'Fruits', ['Food', 'Fruit', 'Apple'], 5))
        #     self.non_empty_cart.products[self.products[i].catalog_number] = {'product': self.products[i], 'amount': 1}

    def test_is_empty(self):
        store = Store('schnitzale', 23444, 4, None, None)
        cart = ShoppingCart(store)
        self.assertTrue(cart.is_empty())
        product = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        store.add_new_product(product)
        store.inc_product_amount(product.catalog_number, 5)
        cart.products[product.catalog_number] = {'product': product, 'amount': 1}
        self.assertFalse(cart.is_empty())

    def test_contains_product(self):
        store = Store('schnitzale', 23444, 4, None, None)
        cart = ShoppingCart(store)
        product = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        self.assertFalse(cart.contains_product(product))
        store.add_new_product(product)
        store.inc_product_amount(product.catalog_number, 5)
        cart.products[product.catalog_number] = {'product': product, 'amount': 1}
        self.assertTrue(cart.contains_product(product))

    def test_add_product(self):
        store = Store('schnitzale', 23444, 4, None, None)
        cart = ShoppingCart(store)
        product = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        store.add_new_product(product)
        store.inc_product_amount(product.catalog_number, 5)
        cart.add_product(product)
        self.assertEqual(cart.products[product.catalog_number], {'product': product, 'amount': 1})
        cart.add_product(product)
        self.assertEqual(cart.products[product.catalog_number], {'product': product, 'amount': 2})

    def test_remove_product(self):
        store = Store('schnitzale', 23444, 4, None, None)
        cart = ShoppingCart(store)
        product = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        store.add_new_product(product)
        store.inc_product_amount(product.catalog_number, 5)
        cart.products[product.catalog_number] = {'product': product, 'amount': 2}
        cart.remove_product(product)
        self.assertEqual(cart.products[product.catalog_number], {'product': product, 'amount': 1})
        cart.remove_product(product)
        self.assertEqual(len(cart.products), 0)

    def test_calculate_price(self):
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store = Store('schnitzale', 23444, 4, discount_service, buying_policy)
        cart = ShoppingCart(store)
        product_a = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        product_b = Product('israeli schnitzel', 'schnitzel', ['hot', 'casher'], 15)
        store.add_new_product(product_a)
        store.inc_product_amount(product_a.catalog_number, 5)
        store.add_new_product(product_b)
        store.inc_product_amount(product_b.catalog_number, 5)
        cart.products[product_a.catalog_number] = {'product': product_a, 'amount': 2}
        self.assertEqual(cart.calculate_price(), 70)
        cart.products[product_b.catalog_number] = {'product': product_b, 'amount': 1}
        self.assertEqual(cart.calculate_price(), 85)



