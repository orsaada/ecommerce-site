import unittest
from src.shopping_cart import ShoppingCart
from src.shopping_basket import ShoppingBasket
from src.discount_service import DiscountService
from src.store import Store
from src.buying_policy_service import BuyingPolicyService
from src.product import Product


class TestShoppingBasket(unittest.TestCase):

    def setUp(self):
        pass
        # self.empty_basket = ShoppingBasket()
        # self.non_empty_basket = ShoppingBasket()
        # self.carts = []
        # self.products = []
        # for i in range(3):
        #     self.carts.append(ShoppingCart(i*10))
        #     for j in range(3):
        #         self.products.append(Product('Apple', 'Fruits', ['Food', 'Fruit', 'Apple'], 5))
        #         self.carts[i].products[self.products[j].catalog_number] = {'product': self.products[j], 'amount': 1}
        #     self.non_empty_basket.shopping_carts.append(self.carts[i])

    def test_is_empty(self):
        basket = ShoppingBasket()
        self.assertTrue(basket.is_empty())
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store = Store('effect', 123, 123, discount_service, buying_policy)
        cart = ShoppingCart(store)
        basket.shopping_carts.append(cart)
        self.assertFalse(basket.is_empty())

    def test_contains_cart(self):
        basket = ShoppingBasket()
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store = Store('effect', 123, 123, discount_service, buying_policy)
        cart = ShoppingCart(store)
        self.assertFalse(basket.contains_cart(cart))
        basket.shopping_carts.append(cart)
        self.assertTrue(basket.contains_cart(cart))

    def test_remove_cart(self):
        basket = ShoppingBasket()
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store = Store('effect', 123, 123, discount_service, buying_policy)
        cart = ShoppingCart(store)
        basket.shopping_carts.append(cart)
        basket.remove_cart(cart)
        self.assertEqual(basket.shopping_carts, [])

    def test_calculate_price(self):
        basket = ShoppingBasket()
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store = Store('effect', 123, 123, discount_service, buying_policy)
        cart = ShoppingCart(store)
        product_a = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        product_b = Product('israeli schnitzel', 'schnitzel', ['hot', 'casher'], 15)
        cart.add_product(product_a)
        basket.shopping_carts.append(cart)
        self.assertEqual(basket.calculate_price(), 35)
        cart.add_product(product_b)
        self.assertEqual(basket.calculate_price(), 50)

    def test_add_product_to_cart(self):
        basket = ShoppingBasket()
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store = Store('effect', 123, 123, discount_service, buying_policy)
        product_a = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        self.assertFalse((basket.add_product_to_cart(product_a, store)).val)
        store.add_new_product(product_a)
        self.assertFalse((basket.add_product_to_cart(product_a, store)).val)
        store.inc_product_amount(product_a.catalog_number, 5)
        self.assertTrue((basket.add_product_to_cart(product_a, store)).val)
        self.assertEqual(len(basket.shopping_carts), 1)
        product_b = Product('israeli schnitzel', 'schnitzel', ['hot', 'casher'], 15)
        store.add_new_product(product_b)
        store.inc_product_amount(product_b.catalog_number, 5)
        self.assertTrue((basket.add_product_to_cart(product_b, store)).val)
        self.assertEqual(len(basket.shopping_carts), 1)
        self.assertEqual(len(basket.shopping_carts[0].products), 2)

    def test_remove_product_from_cart(self):
        basket = ShoppingBasket()
        discount_service = DiscountService()
        buying_policy = BuyingPolicyService()
        store = Store('effect', 123, 123, discount_service, buying_policy)
        product = Product('france schnitzel', 'schnitzel', ['hot', 'crispy'], 35)
        cart = ShoppingCart(store)
        self.assertFalse((basket.remove_product_from_cart(product, cart)).val)
        basket.shopping_carts.append(cart)
        self.assertFalse((basket.remove_product_from_cart(product, cart)).val)
        cart.add_product(product)
        self.assertTrue((basket.remove_product_from_cart(product, cart)).val)

