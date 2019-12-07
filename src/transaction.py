

class Transaction:
    def __init__(self, transaction_id, products, username, payment_method, payment_details, address,
                 account_number, store_number):
        self.transaction_id = transaction_id
        self.total_price = 0
        self.buyer_username = username
        self.products = products
        self.store_number = store_number
        self.store_account = account_number
        self.payment_method = payment_method
        self.payment_details = payment_details
        self.address = address
        self.payment_status = 'unpaid'
        self.delivery_status = 'undelivered'

    def update_payment_status(self):
        self.payment_status = 'paid'

    def update_delivery_status(self):
        self.delivery_status = 'delivered'

    def printer(self):
        return "transaction id " + self.transaction_id + ", total price " + str(self.total_price) + ", buyer username: " \
            + \
            + self.buyer_username \
            + self.products \
            + str(self.store_number) \
            + self.store_account \
            + self.payment_method \
            + self.payment_details \
            + self.address \
            + str(self.payment_status) \
            + str(self.delivery_status)

    # def __repr__(self):
    #     return "transaction id " + self.transaction_id + ", total price " + str(self.total_price) + ", buyer username: "\
    #            + \
    #         + self.buyer_username \
    #         + self.products \
    #         + str(self.store_number)\
    #         + self.store_account\
    #         + self.payment_method \
    #         + self.payment_details \
    #         + self.address \
    #         + str(self.payment_status)\
    #         + str(self.delivery_status)

    def __str__(self):
        return "transaction id " + str(self.transaction_id)


