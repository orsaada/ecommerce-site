import logging
from src.transaction_management import TransactionManagement
from src.delivery_system import DeliverySystem, DeliveryAddress
from src.payments_system import PaymentsSystem
from src.db.db_functions import *


def setup_logger(name, log_file, level):
    handler = logging.FileHandler(log_file)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


logger_ev = setup_logger('event log', 'event.log', logging.INFO)
logger_er = setup_logger('error log', 'error.log', logging.ERROR)


class Ecommerce:
    class __Ecommerce:
        def __init__(self):
            self.delivery_system = DeliverySystem()
            self.payment_system = PaymentsSystem()
            self.transaction_management = TransactionManagement(self.payment_system, self.delivery_system)

        @staticmethod
        def handle_logger(mess):
            if mess.logger_type == 0:
                logger_er.error(mess.message)
            else:
                logger_ev.info(mess.message)
            return mess

        def make_admin(self, username, password, age=0):
            return self.handle_logger(create_new_admin_db(username, password, age))

        def get_stores_of_user_manager(self, username):
            return self.handle_logger(get_stores_of_user_manager_db(username))

        def get_stores_of_user_owner(self, username):
            return self.handle_logger(get_stores_of_user_owner_db(username))

        def search_product(self, attribute: str, value):
            if attribute == 'Category':
                return self.handle_logger(search_products_by_category_db(value))
            if attribute == 'Name':
                return self.handle_logger(search_products_by_name_db(value))
            if attribute == 'Keyword':
                return self.handle_logger(search_products_by_key_word_db(value))

        def is_product_in_store(self, store_number, catalog_number):
            return self.handle_logger(is_product_in_store_db(store_number, catalog_number))

        def add_to_cart(self, username, catalog_number, cart):
            res = add_to_cart_db(username, catalog_number, cart)
            if res is not 1:  # case of subscriber or there is not product with this catalog_number
                return self.handle_logger(res)
            for p in cart['products']:
                if p[0] == catalog_number:
                    x = p
                    cart['products'].remove(p)
                    cart['products'].append((x[0], x[1] + 1, x[2]))
                    return self.handle_logger(MessageResponse(True, 1,
                                                              "The amount of this product increment successfully"))
            cart['products'].append((catalog_number, 1, get_price_db(catalog_number)))
            return self.handle_logger(MessageResponse(True, 1, "New product was added to cart successfully"))

        def remove_from_cart(self, username, catalog_number, cart):
            if cart is None:
                return self.handle_logger(remove_from_cart_db(username, catalog_number))
            for p in cart['products']:
                if p[0] == catalog_number and p[1] > 1:
                    x = p
                    cart['products'].remove(p)
                    cart['products'].append((x[0], x[1] - 1, x[2]))
                    return self.handle_logger(MessageResponse(True, 1,
                                                              "The amount of this product decrement successfully"))
                elif p[0] == catalog_number:
                    cart['products'].remove(p)
                    return self.handle_logger(MessageResponse(True, 1,
                                                              "The product was removed successfully"))
            return self.handle_logger(MessageResponse(False, 1, "No such product in this cart"))

        def show_store(self, store_number):
            return self.handle_logger(show_store_db(store_number))

        def show_cart(self, username, store_number):
            return self.handle_logger(show_cart_db(username, store_number))

        def login(self, username, password):
            x = authentication_db(username, password)
            if x.val is True:
                return self.handle_logger(get_states(username))
            else:
                return self.handle_logger(MessageResponse(None, x.logger_type, x.message))

        def open_new_store(self, name, supervisor_username, account_number, minimum_products,
                           maximum_products, minimum_age):
            return self.handle_logger(open_new_store_db(name, supervisor_username, account_number, minimum_products,
                                                        maximum_products, minimum_age))

        def register(self, username, password, age):
            return self.handle_logger(create_new_user_db(username, password, age))

        def close_permanently(self, username, store_number):
            return self.handle_logger(close_permanently_db(username, store_number))

        def remove_subscriber(self, username, user_to_remove):
            return self.handle_logger(remove_subscriber_db(username, user_to_remove))

        def add_new_product(self, username, product_name, price, amount, category, store_number, key_words,
                            minimum_products, maximum_products, minimum_age):
            if amount <= 0:
                return self.handle_logger(MessageResponse(False, 1, "Illegal amount"))
            if price <= 0:
                return self.handle_logger(MessageResponse(False, 1, "Illegal price"))
            is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
            if is_in_rule is False:
                is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
            if is_in_rule is False:
                return self.handle_logger(MessageResponse(False, 1, "This user cannot add new product to this store"))
            if is_in_rule is True:
                return self.handle_logger(create_new_product_db(product_name, price, amount, category, store_number,
                                                                key_words, minimum_products, maximum_products,
                                                                minimum_age))

            return self.handle_logger(is_in_rule)

        def add_store_owner(self, username_appoints, store_number, username_appointed):
            return self.handle_logger(add_owner_db(username_appoints, username_appointed, store_number))

        def add_store_manager(self, username_appoints, store_number, username_appointed):
            return self.handle_logger(add_manager_db(username_appoints, username_appointed, store_number))

        # def inc_product_amount(self, username, catalog_number, amount):
        #     store_number = get_store_number_by_product_db(catalog_number)
        #     if store_number is False:
        #         return self.handle_logger(MessageResponse(False, 0, "Error while trying getting store_number of product"))
        #     if not amount > 0:
        #         return self.handle_logger(MessageResponse(False, 1, "Illgeal amount"))
        #     is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
        #     if is_in_rule is False:
        #         is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
        #     if is_in_rule is False:
        #         return self.handle_logger(MessageResponse(False, 1, "This user cannot increment the product "
        #                                                         "amount in this store"))
        #     if is_in_rule is True:
        #         return self.handle_logger(inc_product_amount_db(catalog_number, amount))
        #     return self.handle_logger(is_in_rule)
        #
        # def dec_product_amount(self, username, catalog_number, amount):
        #     store_number = get_store_number_by_product_db(catalog_number)
        #     if store_number is False:
        #         return self.handle_logger(MessageResponse(False, 0, "Error while trying getting store_number of product"))
        #     if not amount > 0:
        #         return self.handle_logger(MessageResponse(False, 1, "Illegal amount"))
        #     is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
        #     if is_in_rule is False:
        #         is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
        #     if is_in_rule is False:
        #         return self.handle_logger(MessageResponse(False, 1, "This user cannot decrement the product "
        #                                                         "amount in this store"))
        #     if is_in_rule is True:
        #         return self.handle_logger(dec_product_amount_db(catalog_number, amount))
        #     return self.handle_logger(is_in_rule)

        def remove_product(self, username, catalog_number):
            store_number = get_store_number_by_product_db(catalog_number)
            if store_number is False:
                return self.handle_logger(MessageResponse(False, 0, "Error while trying getting store_number of product"))
            is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
            if is_in_rule is False:
                is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
            if is_in_rule is False:
                return self.handle_logger(MessageResponse(False, 1, "This user cannot decrement the product "
                                                                "amount in this store"))
            if is_in_rule is True:
                return self.handle_logger(remove_product_from_store_db(catalog_number))
            return self.handle_logger(is_in_rule)

        def change_details_of_product(self, username, catalog_number, attribute, value):
            store_number = get_store_number_by_product_db(catalog_number)
            if store_number is False:
                return self.handle_logger(MessageResponse(False, 0, "Error while trying getting store_number of product"))
            is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
            if is_in_rule is False:
                is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
            if is_in_rule is False:
                return self.handle_logger(MessageResponse(False, 1, "This user cannot change product's details"))
            if is_in_rule is not True:
                return self.handle_logger(is_in_rule)
            if attribute == 'Name' or attribute == 'Catgeory':
                value = "'" + value + "'"
                return self.handle_logger(change_details_of_product_db(catalog_number, attribute, value))
            if attribute == 'Price' or attribute == 'Amount' or attribute == 'minimum_products' or \
                    attribute == 'maximum_products' or attribute == 'minimum_age':
                value = int(value)
                if value <= 0:
                    return self.handle_logger(MessageResponse(False, 1, "Illegal value"))
                return self.handle_logger(change_details_of_product_db(catalog_number, attribute, value))
            return self.handle_logger(MessageResponse(False, 1, "Illegal attribute"))

        def remove_store_owner(self, username, store_number, appointed_username):
            return self.handle_logger(remove_store_owner_db(username, store_number, appointed_username))

        def remove_store_manager(self, username, store_number, appointed_username):
            return self.handle_logger(remove_store_manager_db(username, store_number, appointed_username))

        def close_store(self, username, store_number):
            return self.handle_logger(close_store_db(username, store_number))

        def reopen_store(self, username, store_number):
            return self.handle_logger(reopen_store_db(username, store_number))

        def change_details_of_store(self, username, store_number, attribute, value):
            is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
            if is_in_rule is False:
                is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
            if is_in_rule is False:
                return self.handle_logger(MessageResponse(False, 1, "This user cannot change store's details"))
            if is_in_rule is not True:
                return self.handle_logger(is_in_rule)
            if attribute == 'Name':
                value = "'" + value + "'"
                return self.handle_logger(change_details_of_store_db(store_number, attribute, value))
            if attribute == 'Account Number' or attribute == 'minimum_products' or \
                    attribute == 'maximum_products' or attribute == 'minimum_age':
                value = int(value)
                if value < 0:
                    return self.handle_logger(MessageResponse(False, 1, "Illegal value"))
                return self.handle_logger(change_details_of_store_db(store_number, attribute, value))
            return self.handle_logger(MessageResponse(False, 1, "Illegal attribute"))

        def add_reg_discount_of_store(self, username, store_number, discount_percentages, double_deals,
                                      start_time, end_time):
            discount_percentages = int(discount_percentages)
            if discount_percentages > 100 or discount_percentages < 0:
                return self.handle_logger(MessageResponse(False, 1, "Illegal discount percentages"))
            if store_number is False:
                return self.handle_logger(MessageResponse(False, 0, "Error while trying getting store_number "
                                                                    "of product"))
            is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
            if is_in_rule is False:
                is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
            if is_in_rule is False:
                return self.handle_logger(MessageResponse(False, 1, "This user cannot change product's details"))
            if is_in_rule is not True:
                return self.handle_logger(is_in_rule)
            return self.handle_logger(add_reg_discount__of_store_db(store_number, discount_percentages, double_deals,
                                                                    start_time, end_time))

        def add_reg_discount(self, username, catalog_number, discount_percentages, double_deals, start_time, end_time):
            discount_percentages = int(discount_percentages)
            if discount_percentages > 100 or discount_percentages < 0:
                return self.handle_logger(MessageResponse(False, 1, "Illegal discount percentages"))
            store_number = get_store_number_by_product_db(catalog_number)
            if store_number is False:
                return self.handle_logger(MessageResponse(False, 0, "Error while trying getting store_number "
                                                                    "of product"))
            is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
            if is_in_rule is False:
                is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
            if is_in_rule is False:
                return self.handle_logger(MessageResponse(False, 1, "This user cannot change product's details"))
            if is_in_rule is not True:
                return self.handle_logger(is_in_rule)
            return self.handle_logger(add_reg_discount_db(catalog_number, discount_percentages, double_deals,
                                                          start_time, end_time))

        def add_cond_discount(self, username, catalog_number, discount_percentages, double_deals, start_time, end_time,
                              conditional_type, catalog_number_of_second_product):
            discount_percentages = int(discount_percentages)
            if discount_percentages > 100 or discount_percentages < 0:
                return self.handle_logger(MessageResponse(False, 1, "Illegal discount percentages"))
            store_number = get_store_number_by_product_db(catalog_number)
            if store_number is False:
                return self.handle_logger(MessageResponse(False, 0, "Error while trying getting store_number "
                                                                    "of product"))
            is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
            if is_in_rule is False:
                is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
            if is_in_rule is False:
                return self.handle_logger(MessageResponse(False, 1, "This user cannot change product's details"))
            if is_in_rule is not True:
                return self.handle_logger(is_in_rule)
            return self.handle_logger(add_cond_discount_db(catalog_number, discount_percentages, double_deals,
                                                           start_time, end_time, conditional_type,
                                                           catalog_number_of_second_product))

        def add_coupon_discount(self, username, catalog_number, discount_percentages, double_deals, start_time, end_time):
            discount_percentages = int(discount_percentages)
            if discount_percentages > 100 or discount_percentages < 0:
                return self.handle_logger(MessageResponse(False, 1, "Illegal discount percentages"))
            store_number = get_store_number_by_product_db(catalog_number)
            if store_number is False:
                return self.handle_logger(MessageResponse(False, 0, "Error while trying getting store_number "
                                                                        "of product"))
            is_in_rule = is_in_rule_in_the_store_db(username, "STORE_MANAGER", store_number)
            if is_in_rule is False:
                is_in_rule = is_in_rule_in_the_store_db(username, "STORE_OWNER", store_number)
            if is_in_rule is False:
                return self.handle_logger(MessageResponse(False, 1, "This user cannot change product's details"))
            if is_in_rule is not True:
                return self.handle_logger(is_in_rule)
            return self.handle_logger(add_coupon_discount_db(catalog_number, discount_percentages, double_deals,
                                                             start_time, end_time))

        @staticmethod
        def is_legal_shopping_basket(username, shopping_basket):
            for cart in shopping_basket:
                sum_of_amount = 0
                for p in cart['products']:
                    sum_of_amount += p[1]
                    min_amount = get_detail_of_product_db(p[0], "minimum_products")
                    max_amount = get_detail_of_product_db(p[0], "maximum_products")
                    min_age = get_detail_of_product_db(p[0], "minimum_age")
                    if (min_amount > p[1] and min_amount != -1) or (max_amount < p[1] and min_amount != -1) or \
                            (min_age > get_age_of_user_db(username) and min_age != -1):
                        return MessageResponse(False, 1, "This user cannot make the purchase with this cart")
                min_amount = get_detail_of_store_db(cart['store_number'], "minimum_products")
                max_amount = get_detail_of_store_db(cart['store_number'], "maximum_products")
                min_age = get_detail_of_store_db(cart['store_number'], "minimum_age")
                if (min_amount > sum_of_amount and min_amount != -1) or \
                        (max_amount < sum_of_amount and max_amount != -1) or \
                        (min_age > get_age_of_user_db(username) and min_age != -1):
                    return MessageResponse(False, 1, "This user cannot make the purchase with this cart")
            return 1

        # CHANGE IT
        def make_purchase(self, username: str, payment_method: str, payment_details, address: DeliveryAddress,
                          age, basket):
            shopping_basket = []
            stores = get_all_stores_db()

            # build the shopping basket
            for st in stores:
                shopping_cart = show_cart_db(username, st[0])
                if shopping_cart.val is None:
                    return self.handle_logger(shopping_cart)
                if len(shopping_cart.val) > 0:
                    shopping_basket.append({'store_number': st[0], "products": shopping_cart.val})

            if len(shopping_basket) == 0:
                return self.handle_logger(MessageResponse(False, 1, 'Empty basket'))

            # check about min max amount and min age
            is_legal_basket = self.is_legal_shopping_basket(username, shopping_basket)
            if not (is_legal_basket == 1):
                return self.handle_logger(is_legal_basket)

            all_transactions_been_made = []
            for shopping_cart in shopping_basket:
                transaction_made = self.transaction_management.execute_transaction(username, shopping_cart,
                    payment_method, payment_details, address,
                    get_detail_of_store_db(shopping_cart["store_number"], "account_number"))
                self.handle_logger(transaction_made)
                if transaction_made.val is not False:
                    all_transactions_been_made.append(transaction_made.val)
            remove_all_carts(username)
            return self.handle_logger(MessageResponse(all_transactions_been_made, 1,
                                                      "The purchase was made successfully"))

    instance = None

    @staticmethod
    def get_instance():
        if not Ecommerce.instance:
            Ecommerce.instance = Ecommerce.__Ecommerce()
        return Ecommerce.instance
