import unittest
from src.supply_system import SupplySystem
from src.delivery_system import DeliveryAddress


class SupplySystemTest(unittest.TestCase):

    def setUp(self):
        self.ssystem = SupplySystem()

    def test_handshake(self):
        actual = self.ssystem.handshake()
        expected = 'approved'
        self.assertEqual(actual, expected)

    def test_supply(self):
        address = DeliveryAddress(20, "Israel", "Beer Sheva", "Rager Blvd 12", "8458527")
        actual = self.ssystem.supply("Israel Israelovice", address)
        expected = 'approved'
        self.assertEqual(actual, expected)
