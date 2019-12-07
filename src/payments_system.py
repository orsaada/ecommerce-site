import requests


class PaymentsSystem:

    URL = "https://cs-bgu-wsep.herokuapp.com/"

    def __init__(self):
        print("Payments system stub is working!")

    def handshake(self):
        handshake_data = {
            'action_type': 'handshake'
        }
        response = requests.post(url=self.URL, data=handshake_data)
        if response.status_code == 200 and response.text == 'OK':
            return 'approved'
        return 'error'

    def pay(self, identifier: str, card_number: str, holder: str, ccv: str, month: str, year: str):
        payment_data = {
            "action_type": "pay",
            "card_number": card_number,
            "month": month,
            "year": year,
            "holder": holder,
            "ccv": ccv,
            "id": identifier
        }
        response = requests.post(url=self.URL, data=payment_data)
        if response.status_code == 200 and int(response.text) != -1:
            return 'approved'
        return 'error'

    def charge(self, identifier: int, holder: str, card_number: str, month: str, year: str, ccv: str):
        self.handshake()
        return self.pay(str(identifier), card_number, holder, ccv, month, year)
