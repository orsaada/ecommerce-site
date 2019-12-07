import unittest
import datetime
from src.discount_service import DiscountService
from src.product import Product
from src.shopping_cart import ShoppingCart
from src.store import Store


class TestDiscountService(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_product_discount(self):
        discount = DiscountService()
        apple = Product('apple', 'fruit', ['green', 'sweet'], 5)
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        discount.add_product_discount(apple, 70, True, start_date, end_date)
        self.assertEqual(len(discount.product_discount_table), 1)
        self.assertTrue(discount.product_discount_table[apple.catalog_number]['RegularDiscount'][discount.DISCOUNT_TYPE]
                        == 'RegularDiscount')
        self.assertEqual(discount.product_discount_table[apple.catalog_number]['RegularDiscount']
                         [discount.DISCOUNT_PERCENTAGE], 70)
        self.assertTrue(discount.product_discount_table[apple.catalog_number]['RegularDiscount']
                        [discount.DOUBLE_DEALS])
        discount.add_product_discount(apple, 60, False, start_date, end_date, coupon_code=123)
        self.assertEqual(len(discount.product_discount_table), 1)
        self.assertTrue(discount.product_discount_table[apple.catalog_number]['CouponDiscount'][discount.DISCOUNT_TYPE]
                        == 'CouponDiscount')
        self.assertTrue(discount.product_discount_table[apple.catalog_number]['CouponDiscount']
                        [discount.DISCOUNT_PERCENTAGE], 60)
        self.assertFalse(discount.product_discount_table[apple.catalog_number]['CouponDiscount']
                         [discount.DOUBLE_DEALS])

    def test_has_regular_product_discount(self):
        discount = DiscountService()
        apple = Product('apple', 'fruit', ['green', 'sweet'], 5)
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        self.assertFalse(discount.has_regular_product_discount(apple))
        discount.add_product_discount(apple, 70, True, start_date, end_date)
        self.assertTrue(discount.has_regular_product_discount(apple))

    def test_has_conditional_product_discount(self):
        discount = DiscountService()
        apple = Product('apple', 'fruit', ['green', 'sweet'], 5)
        mango = Product('mango', 'fruit', ['yellow', 'sweet'], 7)
        pear = Product('pear', 'fruit', ['green', 'sweet'], 4)
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        self.assertFalse(discount.has_conditional_product_discount(apple))
        discount.add_product_discount(apple, 70, True, start_date, end_date, condition=('And', pear, mango))
        self.assertTrue(discount.has_conditional_product_discount(apple))

    def test_has_coupon_product_discount(self):
        discount = DiscountService()
        apple = Product('apple', 'fruit', ['green', 'sweet'], 5)
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        self.assertFalse(discount.has_coupon_product_discount(apple))
        discount.add_product_discount(apple, 70, True, start_date, end_date, coupon_code=123)
        self.assertTrue(discount.has_coupon_product_discount(apple))

    def test_delete_regular_product_discount(self):
        discount = DiscountService()
        apple = Product('apple', 'fruit', ['green', 'sweet'], 5)
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        discount.add_product_discount(apple, 70, True, start_date, end_date, coupon_code=123)
        self.assertTrue(discount.has_coupon_product_discount(apple))
        discount.delete_coupon_product_discount(apple)
        self.assertFalse(discount.has_coupon_product_discount(apple))

    def test_delete_condition_product_discount(self):
        discount = DiscountService()
        apple = Product('apple', 'fruit', ['green', 'sweet'], 5)
        mango = Product('mango', 'fruit', ['yellow', 'sweet'], 7)
        pear = Product('pear', 'fruit', ['green', 'sweet'], 4)
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        discount.add_product_discount(apple, 70, True, start_date, end_date, condition=('And', pear, mango))
        self.assertTrue(discount.has_conditional_product_discount(apple))
        discount.delete_conditional_product_discount(apple)
        self.assertFalse(discount.has_conditional_product_discount(apple))

    def test_delete_coupon_product_discount(self):
        discount = DiscountService()
        apple = Product('apple', 'fruit', ['green', 'sweet'], 5)
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        discount.add_product_discount(apple, 70, True, start_date, end_date, coupon_code=123)
        self.assertTrue(discount.has_coupon_product_discount(apple))
        discount.delete_coupon_product_discount(apple)
        self.assertFalse(discount.has_coupon_product_discount(apple))

    def test_add_store_discount(self):
        discount = DiscountService()
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        self.assertEqual(discount.store_discount, None)
        discount.store_discount = ('StoreDiscount', 70, True, start_date, end_date)
        self.assertTrue(discount.store_discount[discount.DISCOUNT_TYPE] == 'StoreDiscount')
        self.assertEqual(discount.store_discount[discount.DISCOUNT_PERCENTAGE], 70)
        self.assertTrue(discount.store_discount[discount.DOUBLE_DEALS])

    def test_has_store_discount(self):
        discount = DiscountService()
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        self.assertFalse(discount.has_store_discount())
        discount.store_discount = ('StoreDiscount', 70, True, start_date, end_date)
        self.assertTrue(discount.has_store_discount())

    def test_delete_store_discount(self):
        discount = DiscountService()
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        discount.store_discount = ('StoreDiscount', 70, True, start_date, end_date)
        self.assertTrue(discount.has_store_discount())
        discount.delete_store_discount()
        self.assertFalse(discount.has_store_discount())

    def test_calculate_product_discount_percentage(self):
        store = Store('effect', 123, 123, None, None)
        discount = DiscountService()
        apple = Product('apple', 'fruit', ['green', 'sweet'], 5)
        shopping_cart = ShoppingCart(store)
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        discount.store_discount = ('StoreDiscount', 10, True, start_date, end_date)
        discount.add_product_discount(apple, 20, True, start_date, end_date, coupon_code=123)
        x = discount.calculate_product_discount_percentage(apple, shopping_cart)
        self.assertEqual(x[0], 30)
        self.assertEqual(x[1], ['CouponDiscount', 'StoreDiscount'])
        discount.add_product_discount(apple, 45, False, start_date, end_date)
        x = discount.calculate_product_discount_percentage(apple, shopping_cart)
        self.assertEqual(x[0], 45)
        self.assertEqual(x[1], ['RegularDiscount'])

    def test_calculate_individual_discount(self):
        discount = DiscountService()
        apple = Product('apple', 'fruit', ['green', 'sweet'], 5)
        shopping_cart = ShoppingCart(Store('effect', 123, 123, None, None))
        start_date = datetime.datetime(2016, 2, 1, 12, 12, 12, 12)
        end_date = datetime.datetime(2020, 2, 1, 12, 12, 12, 12)
        discount.add_product_discount(apple, 20, True, start_date, end_date, coupon_code=123)
        x = discount.calculate_individual_discount(discount.product_discount_table[apple.catalog_number]
                                                   ['CouponDiscount'], shopping_cart)
        self.assertEqual(x[0], 20)
        self.assertEqual(x[1], 'CouponDiscount')

    def test_check_conditional_discount(self):
        discount = DiscountService()
        mango = Product('mango', 'fruit', ['yellow', 'sweet'], 7)
        pear = Product('pear', 'fruit', ['green', 'sweet'], 4)
        shopping_cart = ShoppingCart(Store('effect', 123, 123, None, None))
        shopping_cart.add_product(mango)
        self.assertFalse(discount.check_conditional_discount(('And', pear, mango), shopping_cart))
        shopping_cart.add_product(pear)
        self.assertTrue(discount.check_conditional_discount(('And', pear, mango), shopping_cart))

