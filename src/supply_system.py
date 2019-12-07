import requests
from src.delivery_system import DeliveryAddress


class SupplySystem:

    URL = "https://cs-bgu-wsep.herokuapp.com/"

    def __init__(self):
        print("Supply system stub is working!")

    def handshake(self):
        handshake_data = {
            'action_type': 'handshake'
        }
        response = requests.post(url=self.URL, data=handshake_data)
        if response.status_code == 200 and response.text == 'OK':
            return 'approved'
        return 'error'

    def supply(self, name: str, address: DeliveryAddress):
        supply_data = {
            "action_type": "supply",
            "name": name,
            "address": address.full_address['street'],
            "city": address.full_address['city'],
            "country": address.full_address['country'],
            "zip": address.full_address['postal_code']
        }

        response = requests.post(url=self.URL, data=supply_data)
        if response.status_code == 200 and int(response.text) != -1:
            return 'approved'
        return 'error'
