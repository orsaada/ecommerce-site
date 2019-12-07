import datetime
from src.db.db_functions import *


class ShoppingCart:

    def __init__(self, store_number, products):
        self.store_number = store_number
        self.products = products
        self.discount_service = None
        self.build_discount_service()

    def build_discount_service(self):
        self.discount_service = DiscountService()
        discount = get_reg_discount_of_store_db(self.store_number)
        if not (discount is False):
            self.discount_service.add_store_discount(discount[1], discount[2],
                                                     datetime.datetime.strptime(discount[3], '%Y-%m-%d'),
                                                     datetime.datetime.strptime(discount[4], '%Y-%m-%d'))
        for p in self.products:
            discount = get_reg_discount_of_product_db(p[0])
            print('discount: ', discount)
            if not (discount is False):
                self.discount_service.add_product_discount(discount[0], discount[1], discount[2],
                                                           datetime.datetime.strptime(discount[3], '%Y-%m-%d'),
                                                           datetime.datetime.strptime(discount[4], '%Y-%m-%d'))
            discount = get_cond_discount_of_product_db(p[0])
            if not (discount is False):
                self.discount_service.add_product_discount(discount[0], discount[1], discount[2],
                                                           datetime.datetime.strptime(discount[3], '%Y-%m-%d'),
                                                           datetime.datetime.strptime(discount[4], '%Y-%m-%d'),
                                                           condition=(discount[5], p[0], discount[6]))
            discount = get_coupon_discount_of_product_db(p[0])
            if not (discount is False):
                self.discount_service.add_product_discount(discount[0], discount[1], discount[2],
                                                           datetime.datetime.strptime(discount[3], '%Y-%m-%d'),
                                                           datetime.datetime.strptime(discount[4], '%Y-%m-%d'),
                                                           coupon_code=123)

        print('\nproduct_discount_table: ', self.discount_service.product_discount_table)
        print('\nstore_discount: ', self.discount_service.store_discount)

    def calculate_price(self):
        price_sum = 0
        for product_dict in self.products:
            discount_percentage = \
                self.discount_service.calculate_product_discount_percentage(product_dict[0], self)
            discount_percentage = discount_percentage[0]

            print('\ndiscount_percentage:', discount_percentage)

            if discount_percentage > 80:
                discount_percentage = 80
            price_sum += (product_dict[2] * ((100 - discount_percentage) / 100)) * product_dict[1]
        return price_sum

    def contains_product(self, catalog_number):
        for p in self.products:
            if p[0] == catalog_number:
                return True
        return False

from src.discount_service import DiscountService
