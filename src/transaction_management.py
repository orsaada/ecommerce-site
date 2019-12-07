from src.transaction import Transaction
from src.delivery_system import DeliverySystem, DeliveryAddress
from src.payments_system import PaymentsSystem
from src.shopping_cart import ShoppingCart
from src.message_response import MessageResponse
from src.db.db_functions import *


class TransactionManagement:
    transaction_counter = 0
    transactions = []

    def __init__(self, payment_system: PaymentsSystem, delivery_system: DeliverySystem):
        self.payment_system = payment_system
        self.delivery_system = delivery_system

    @staticmethod
    def check_availability_of_products(shopping_cart):
        for p in shopping_cart["products"]:
            if get_detail_of_product_db(p[0], "amount") < p[1]:
                return False
        return True

    @staticmethod
    def remove_products_from_store(shopping_cart):
        for p in shopping_cart['products']:
            amount_in_store = get_detail_of_product_db(p[0], "amount")
            if amount_in_store == p[1]:
                remove_product_from_store_db(p[0])
            else:
                dec_product_amount_db(p[0], p[1])

    def execute_transaction(self, username: str, shopping_cart, payment_method: str,
                            payment_details, address: DeliveryAddress, account_number: int):
        if not self.check_availability_of_products(shopping_cart):
            return MessageResponse(False, 1, "Not all the products are available in this amount")
        TransactionManagement.transaction_counter += 1
        transaction = Transaction(self.transaction_counter, shopping_cart['products'], username, payment_method,
                                  payment_details, address, account_number, shopping_cart['store_number'])
        cart = ShoppingCart(shopping_cart["store_number"], shopping_cart['products'])
        # until here yet
        transaction.total_price = cart.calculate_price()
        if self.payment_system.charge(username, payment_details[0], payment_details[1], payment_details[2],
                                      payment_details[3], payment_details[4]) == 'declined':
            return MessageResponse(False, 1, "payment problem")
        transaction.update_payment_status()
        if self.delivery_system.delivery(transaction.products, address) == 'undelivered':
            return MessageResponse(False, 1, 'delivery problem, payment were cancelled')
        transaction.update_delivery_status()
        self.transactions.append(transaction)
        self.remove_products_from_store(shopping_cart)
        return MessageResponse(transaction, 1, 'succeed transaction' + str(transaction.transaction_id))

    def get_transactions(self):
        return self.transactions

    def get_transactions_by_store(self, store_number):
        store_transactions = []
        for transaction in self.transactions:
            if transaction.store_number == store_number:
                store_transactions.append(transaction)
        return store_transactions

    def get_transactions_by_identifier(self, identifier):
        buyer_transactions = []
        for transaction in self.transactions:
            if transaction.buyer_identifier == identifier:
                buyer_transactions.append(transaction)
        return buyer_transactions
