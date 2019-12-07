import unittest

from src.delivery_system import DeliveryAddress
from src.ecommerce import Ecommerce
from src.db.db_functions import *


class AcceptanceTest(unittest.TestCase):
    def setUp(self):
        SQL.setTestDb()
        SQLHandler.get_instance().setTestDb()
        emptied = False
        while not emptied:
            emptied = empty_tables().val

    def test_register_happy(self): #ok
        self.assertTrue(Ecommerce.get_instance().register("amirdimri2", "123456789", 24).val, "need return True")

    def test_register_sad(self): #ok
        self.assertFalse(Ecommerce.get_instance().register("roie", "12", "13 24").val, "need return False")

    def test_login_happy(self): #ok
        Ecommerce.get_instance().register("amirdimri", "123456789",23)
        self.assertTrue(Ecommerce.get_instance().login("amirdimri", "123456789"), "need return True")

    def test_login_sad(self):
        Ecommerce.get_instance().register("amirdimri", "123456789",24)
        self.assertFalse(Ecommerce.get_instance().login("amirdimri", "1234").val, "need return False")

    def test_search_product_sad(self): #ok
        Ecommerce.get_instance().register("amirdimri2", "123456789", 24)
        Ecommerce.get_instance().login("amirdimri2", "123456789")
        store_number_response = Ecommerce.get_instance().open_new_store("ramiLevi","amirdimri2","12344",0,15,14)
        print(store_number_response.message)
        catalog_number = Ecommerce.get_instance().add_new_product("seller", 'chocholate', 10, 13, 'Food', store_number_response.val,
                                                 ['food','sweet'], 0, 100, 16).val
        self.assertTrue(Ecommerce.get_instance().search_product("Name", "Banana").val == [])

    def test_add_to_cart_happy(self): #ok
        Ecommerce.get_instance().register("client", "123456789", 24)
        Ecommerce.get_instance().register("seller", "123456789", 24)
        store_number = Ecommerce.get_instance().open_new_store("gifts store","seller","226333",0,100,18).val[0][0]
        print('store number' +str(store_number))
        Ecommerce.get_instance().add_new_product("seller", 'chocholate', 10, 13, 'Food', store_number,
                                                 ['food','sweet'], 0, 100, 16)
        catalog_number = Ecommerce.get_instance().search_product('Name','chocholate').val[0][0]
        print('catalog_number ' + str(catalog_number))
        add_cart_response = Ecommerce.get_instance().add_to_cart("client", catalog_number, None)
        print(add_cart_response.message)

    def test_add_to_cart_sad(self): #ok
        Ecommerce.get_instance().register("client", "123456789", 24)
        self.assertFalse(Ecommerce.get_instance().add_to_cart("client", 17, None).val, "need return False")

    def test_make_purchase(self):
        Ecommerce.get_instance().register('ofek', 'secret', 20)
        Ecommerce.get_instance().login('ofek', 'secret')

        store_number = Ecommerce.get_instance().open_new_store('mystore', 'ofek', 123456, 1, 100, 12).val[0][0]

        Ecommerce.get_instance().add_new_product('ofek', 'mystery book', 50, 17, 'reading', store_number,
                                                 ['mystery', 'leisure'], 1, 70, 13)
        Ecommerce.get_instance().add_new_product('ofek', 'mystery book2', 10, 10, 'reading', store_number,
                                                 ['mystery', 'leisure'], 1, 70, 13)

        catalog_number = (Ecommerce.get_instance().search_product('Name', 'mystery book')).val[0][0]
        catalog_number2 = (Ecommerce.get_instance().search_product('Name', 'mystery book2')).val[0][0]

        Ecommerce.get_instance().add_to_cart('ofek', catalog_number, None)
        Ecommerce.get_instance().add_to_cart('ofek', catalog_number2, None)

        address = DeliveryAddress(100, 'Israel', 'Beer Sheva', 'Rager', '12345')
        print('is', str(Ecommerce.get_instance().make_purchase('ofek', 'paypal',['1234', 'ofek ash', '356', '4', '2022'],
                                                           address, None, None).val[0]))

    def test_open_new_store_happy(self): #ok
        Ecommerce.get_instance().register("client", "123456789", 24)
        Ecommerce.get_instance().register("seller", "123456789", 24)
        store_number = Ecommerce.get_instance().open_new_store("gifts store","seller","226333",0,100,18).val[0][0]
        print(store_number)
        self.assertTrue(store_number > 0)

    def test_add_new_product_happy(self): #ok
        Ecommerce.get_instance().register("client", "123456789", 24)
        Ecommerce.get_instance().register("seller", "123456789", 24)
        store_number = Ecommerce.get_instance().open_new_store("gifts store","seller","226333",0,100,18).val[0][0]
        print(store_number)
        catalog_number = Ecommerce.get_instance().add_new_product("seller", 'chocholate', 10, 13, 'Food', store_number,
                                                     ['food','sweet'], 0, 100, 16).val
        self.assertTrue(catalog_number)

    def test_remove_product_sad(self):
        Ecommerce.get_instance().register("client", "123456789", 24)
        Ecommerce.get_instance().register("seller", "123456789", 24)
        store_number = Ecommerce.get_instance().open_new_store("gifts store","seller","226333",0,100,18).val[0][0]
        print(store_number)
        catalog_number = Ecommerce.get_instance().add_new_product("seller", 'chocholate', 10, 13, 'Food', store_number,
                                                     ['food','sweet'], 0, 100, 16).val
        self.assertFalse(Ecommerce.get_instance().remove_product("seller",catalog_number+1).val)

    def test_change_details_of_product_happy(self):
        Ecommerce.get_instance().register("client", "123456789", 24)
        Ecommerce.get_instance().register("seller", "123456789", 24)
        store_number = Ecommerce.get_instance().open_new_store("gifts store","seller","226333",0,100,18).val[0][0]
        print(store_number)
        catalog_number = Ecommerce.get_instance().add_new_product("seller", 'chocholate', 10, 13, 'Food', store_number,
                                                     ['food','sweet'], 0, 100, 16).val
        self.assertTrue(Ecommerce.get_instance().change_details_of_product("seller",catalog_number,"Name",
                                                                           "brown chocholate"), "need return True")

    def test_appointment_store_owner_happy(self):
        Ecommerce.get_instance().register("seller", "123456789", 24)
        Ecommerce.get_instance().register("notowneryet", "123456789", 24)
        store_number = Ecommerce.get_instance().open_new_store("gifts store","seller","226333",0,100,18).val[0][0]
        Ecommerce.get_instance().add_store_owner("seller",store_number,"notowneryet")

    def test_appointment_store_owner_sad(self):
        Ecommerce.get_instance().register("seller", "123456789", 24)
        Ecommerce.get_instance().register("notowneryet", "123456789", 24)
        store_number = Ecommerce.get_instance().open_new_store("gifts store", "seller", "226333", 0, 100, 18).val[0][0]
        Ecommerce.get_instance().add_store_owner("seller", store_number, "notowneryet")
        Ecommerce.get_instance().add_store_owner("seller", store_number, "notowneryet").val

    def test_remove_store_owner_happy(self):
        Ecommerce.get_instance().register("seller", "123456789", 24)
        Ecommerce.get_instance().register("notowneryet", "123456789", 24)
        store_number = Ecommerce.get_instance().open_new_store("gifts store", "seller", "226333", 0, 100, 18).val[0][0]
        Ecommerce.get_instance().add_store_owner("seller", store_number, "notowneryet")
        self.assertTrue(Ecommerce.get_instance().remove_store_owner("seller",store_number,"notowneryet"))

    def test_appointment_store_manager_happy(self):
        Ecommerce.get_instance().register("seller", "123456789", 24)
        Ecommerce.get_instance().register("notowneryet", "123456789", 24)
        store_number = Ecommerce.get_instance().open_new_store("gifts store", "seller", "226333", 0, 100, 18).val[0][0]
        self.assertTrue( Ecommerce.get_instance().add_store_manager("seller",store_number,"notowneryet"))
