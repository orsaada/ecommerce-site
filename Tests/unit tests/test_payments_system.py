import unittest
from src.payments_system import PaymentsSystem


class PaymentsSystemTest(unittest.TestCase):

    def setUp(self):
        self.psystem = PaymentsSystem()

    def test_handshake(self):
        actual = self.psystem.handshake()
        expected = 'approved'
        self.assertEqual(actual, expected)

    def test_pay(self):
        actual = self.psystem.pay("20444444", "2222333344445555", "Israel Israelovice", "262", "4", "2021")
        expected = 'approved'
        self.assertEqual(actual, expected)

    def test_charge(self):
        actual2 = self.psystem.charge(20444444, "Israel Israelovice", "2222333344445555", "4", "2021", "262")
        expected = 'approved'
        self.assertEqual(actual2, expected)
