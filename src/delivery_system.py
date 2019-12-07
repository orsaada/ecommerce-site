
class DeliveryAddress:
    def __init__(self, delivery_price: int, country: str, city: str = None, street: str = None, postal_code: str = None):
        self.full_address = {
            'country': country,
            'city': city,
            'street': street,
            'postal_code': postal_code
        }
        self.delivery_price = delivery_price


class DeliverySystem:
    def __init__(self):
        print("delivery system stub is working!")

    @staticmethod
    def delivery(products, address):
        if len(products) == 0 or address is None:
            return 'undelivered'
        return "delivered"
