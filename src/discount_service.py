import datetime
from src.shopping_cart import ShoppingCart


class DiscountService:

    DISCOUNT_TYPE = 0
    DISCOUNT_PERCENTAGE = 1
    DOUBLE_DEALS = 2
    START_TIME = 3
    END_TIME = 4
    CONDITION = 5
    COUPON_CODE = 5

    # Product Discount type may be: 'RegularDiscount' | 'ConditionalDiscount' | 'CouponDiscount' (Next Version)
    # Maybe add error testing on input!!!!
    # Remember to update tables upon removing a product from the system
    # Maybe delete the discount type and add a method for each type separately
    # Maybe change the constructor to have a store like in buying policy

    def __init__(self):
        self.product_discount_table = {}
        self.store_discount = None

    def add_product_discount(self, catalog_number, discount_percentage: int,
                             double_deals: bool, start_time, end_time,
                             condition: tuple = None, coupon_code: int = None):
        if catalog_number not in self.product_discount_table:
            self.product_discount_table[catalog_number] = {}
        if condition is not None and coupon_code is not None: # Error! Cant be coupon discount and conditional at once
            return
        if condition is not None:
            self.product_discount_table[catalog_number]['ConditionalDiscount'] = ('ConditionalDiscount',
                                                                                  discount_percentage, double_deals,
                                                                                  start_time, end_time, condition)
        elif coupon_code is not None:
            self.product_discount_table[catalog_number]['CouponDiscount'] = ('CouponDiscount',
                                                                             discount_percentage, double_deals,
                                                                             start_time, end_time, coupon_code)
        else:
            self.product_discount_table[catalog_number]['RegularDiscount'] = ('RegularDiscount',
                                                                              discount_percentage, double_deals,
                                                                              start_time, end_time)

    # REGULAR DISCOUNT:

    def has_regular_product_discount(self, catalog_number):
        return catalog_number in self.product_discount_table \
               and 'RegularDiscount' in self.product_discount_table[catalog_number]

    def delete_regular_product_discount(self, catalog_number):
        if self.has_regular_product_discount(catalog_number):
            del self.product_discount_table[catalog_number]['RegularDiscount']

    # CONDITIONAL DISCOUNT:

    def has_conditional_product_discount(self, catalog_number):
        return catalog_number in self.product_discount_table \
               and 'ConditionalDiscount' in self.product_discount_table[catalog_number]

    def delete_conditional_product_discount(self, catalog_number):
        if self.has_conditional_product_discount(catalog_number):
            del self.product_discount_table[catalog_number]['ConditionalDiscount']

    # COUPON DISCOUNT:

    def has_coupon_product_discount(self, catalog_number):
        return catalog_number in self.product_discount_table \
               and 'CouponDiscount' in self.product_discount_table[catalog_number]

    def delete_coupon_product_discount(self, catalog_number):
        if self.has_coupon_product_discount(catalog_number):
            del self.product_discount_table[catalog_number]['CouponDiscount']

    # STORE DISCOUNT:

    def add_store_discount(self, discount_percentage: int, double_deals: bool,
                           start_time, end_time):
        self.store_discount = ('StoreDiscount', discount_percentage, double_deals, start_time, end_time)

    def has_store_discount(self):
        return self.store_discount is not None

    def delete_store_discount(self):
        self.store_discount = None

    # DISCOUNT CALCULATION METHODS:

    def calculate_product_discount_percentage(self, catalog_number,
                                              shopping_cart: ShoppingCart):

        print('\nin calculate_product_discount_percentage: ', catalog_number, '  ', shopping_cart)

        if not self.has_conditional_product_discount(catalog_number) and not \
                self.has_coupon_product_discount(catalog_number) and not \
                self.has_regular_product_discount(catalog_number) and not self.has_store_discount():
            return 0, 'No Discount'
        max_individual_discount = (0, 'NoDiscount')
        max_double_deal_discount = (0, [])
        all_discounts = list(self.product_discount_table[catalog_number].values())
        if self.has_store_discount():
            all_discounts.append(self.store_discount)
        for discount in all_discounts:
            temp_individual_discount = self.calculate_individual_discount(discount, shopping_cart)
            if temp_individual_discount[0] > max_individual_discount[0]:
                max_individual_discount = temp_individual_discount
            if discount[DiscountService.DOUBLE_DEALS] and temp_individual_discount[0] > 0:
                max_double_deal_discount[1].append(temp_individual_discount[1])
                max_double_deal_discount = (max_double_deal_discount[0] + temp_individual_discount[0],
                                            max_double_deal_discount[1])
        return max_double_deal_discount if max_double_deal_discount[0] > max_individual_discount[0] \
            else (max_individual_discount[0], [max_individual_discount[1]])

    def calculate_individual_discount(self, discount,  shopping_cart: ShoppingCart):
        if datetime.date.today() < discount[DiscountService.START_TIME].date() \
                or datetime.date.today() > discount[DiscountService.END_TIME].date() \
                or (discount[DiscountService.DISCOUNT_TYPE] == 'ConditionalDiscount'
                    and not self.check_conditional_discount(discount[DiscountService.CONDITION], shopping_cart)):
            return 0, 'NoDiscount'
        return discount[DiscountService.DISCOUNT_PERCENTAGE], discount[DiscountService.DISCOUNT_TYPE]

    def check_conditional_discount(self, condition, shopping_cart: ShoppingCart):
        if isinstance(condition, int):
            return shopping_cart.contains_product(condition)
        elif condition[0] == 'Or':
            return self.check_conditional_discount(condition[1], shopping_cart) or \
                   self.check_conditional_discount(condition[2], shopping_cart)
        elif condition[0] == 'And':
            return self.check_conditional_discount(condition[1], shopping_cart) and \
                   self.check_conditional_discount(condition[2], shopping_cart)
