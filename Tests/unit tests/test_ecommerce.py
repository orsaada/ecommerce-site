import unittest
from src.ecommerce import Ecommerce
from src.db.db_functions import *
from src.delivery_system import DeliveryAddress
from src.discount_service import DiscountService


class TestEcommerce(unittest.TestCase):

    def setUp(self):
        SQLHandler.get_instance().setTestDb()
        emptied = False
        while not emptied:
            emptied = empty_tables().val

    def test_search_product(self):
        # no such product
        self.assertEqual(Ecommerce.get_instance().search_product('Name', 'no such product bla bla bla').val, [])

        # search by name
        Ecommerce.get_instance().register('ofek', 'secret', 20)
        store_number = Ecommerce.get_instance().open_new_store('mystore', 'ofek', 123456, 1, 100, 12).val[0][0]
        Ecommerce.get_instance().add_new_product('ofek', 'mystery book', 50, 17, 'reading', store_number,
                                                 ['mystery', 'leisure'], 1, 70, 13)
        self.assertEqual(Ecommerce.get_instance().search_product('Name', 'mystery book').val[0].name, 'mystery book')

        # search by category
        self.assertEqual(Ecommerce.get_instance().search_product('Category', 'reading').val[0].category, 'reading')

        # search by key words
        self.assertEqual(Ecommerce.get_instance().search_product('Keyword', 'mystery').val[0][1], 'mystery')

    def test_add_product_to_cart(self):
        Ecommerce.get_instance().register('ofek', 'secret', 20)
        store_number = Ecommerce.get_instance().open_new_store('mystore', 'ofek', 123456, 1, 100, 12).val[0][0]
        Ecommerce.get_instance().add_new_product('ofek', 'mystery book', 50, 17, 'reading', store_number,
                                                 ['mystery', 'leisure'], 1, 70, 13)
        catalog_number = (Ecommerce.get_instance().search_product('Name', 'mystery book')).val[0][0]

        self.assertTrue(Ecommerce.get_instance().add_to_cart('ofek', catalog_number, None))
        self.assertTrue(len(SQLHandler.get_instance().select_from_db('select * from shopping_carts')) == 1)

    def test_remove_product_from_cart(self):
        Ecommerce.get_instance().register('ofek', 'secret', 20)
        store_number = Ecommerce.get_instance().open_new_store('mystore', 'ofek', 123456, 1, 100, 12).val[0][0]
        Ecommerce.get_instance().add_new_product('ofek', 'mystery book', 50, 17, 'reading', store_number,
                                                 ['mystery', 'leisure'], 1, 70, 13)
        catalog_number = (Ecommerce.get_instance().search_product('Name', 'mystery book')).val[0][0]

        self.assertTrue(Ecommerce.get_instance().add_to_cart('ofek', catalog_number, None))
        self.assertTrue(len(SQLHandler.get_instance().select_from_db('select * from shopping_carts')) == 1)

        self.assertTrue(Ecommerce.get_instance().remove_from_cart('ofek', catalog_number, None))
        self.assertTrue(len(SQLHandler.get_instance().select_from_db('select * from shopping_carts')) == 0)

    def test_show_cart(self):
        Ecommerce.get_instance().register('ofek', 'secret', 20)
        store_number = Ecommerce.get_instance().open_new_store('mystore', 'ofek', 123456, 1, 100, 12).val[0][0]
        Ecommerce.get_instance().add_new_product('ofek', 'mystery book', 50, 17, 'reading', store_number,
                                                 ['mystery', 'leisure'], 1, 70, 13)
        print(Ecommerce.get_instance().show_cart('ofek', store_number).__dict__)

    def test_login(self):
        Ecommerce.get_instance().register('ofek', 'secret', 20)
        self.assertEqual((Ecommerce.get_instance().login('ofek', 'secret')).val, [])

    def test_open_new_store(self):
        Ecommerce.get_instance().register('ofek', 'secret', 20)
        Ecommerce.get_instance().login('ofek', 'secret')
        store_number = Ecommerce.get_instance().open_new_store('mystore', 'ofek', 123456, 1, 100, 12).val[0][0]
        self.assertTrue(store_number is not None)

    def test_register(self):
        self.assertTrue(Ecommerce.get_instance().register('ofek', 'secret', 20))

    def test_close_permanently(self):
        Ecommerce.get_instance().register('ofek', 'secret', 20)

        # real store
        store_number = Ecommerce.get_instance().open_new_store('mystore', 'ofek', 123456, 1, 100, 12).val[0][0]
        Ecommerce.get_instance().make_admin('ofek', 'secret', 20)

        self.assertTrue(Ecommerce.get_instance().close_permanently('ofek', store_number).val)

        new_num_of_stores = SQLHandler.get_instance().select_from_db('select count(*) from stores where store_number = '+ str(store_number))[0][0]
        self.assertEqual(new_num_of_stores, 0)

    def test_remove_subscriber(self):
        Ecommerce.get_instance().make_admin('admin', 'admin', 20)

        Ecommerce.get_instance().register('ofek', 'secret', 20)
        Ecommerce.get_instance().login('ofek', 'secret')

        Ecommerce.get_instance().register('roie', 'bla3', 20)
        Ecommerce.get_instance().login('roie', 'bla3')

        self.assertTrue((Ecommerce.get_instance().remove_subscriber('admin', 'ofek')).val)
        new_num_of_users = SQLHandler.get_instance().select_from_db('select count(*) from users')[0][0]
        self.assertEqual(new_num_of_users, 2)

        self.assertTrue((Ecommerce.get_instance().remove_subscriber('admin', 'roie')).val)
        new_num_of_users = SQLHandler.get_instance().select_from_db('select count(*) from users')[0][0]
        self.assertEqual(new_num_of_users, 1)

    def test_add_new_product(self):
        Ecommerce.get_instance().register('ofek', 'secret', 20)
        store_number = Ecommerce.get_instance().open_new_store('mystore', 'ofek', 123456, 1, 100, 12).val[0][0]
        Ecommerce.get_instance().add_new_product('ofek', 'mystery book', 50, 17, 'reading', store_number,
                                                 ['mystery', 'leisure'], 1, 70, 13)

        self.assertEqual(Ecommerce.get_instance().search_product('Name', 'mystery book').val[0].name, 'mystery book')

        num_of_products = SQLHandler.get_instance().select_from_db('select count(*) from products')[0][0]
        self.assertEqual(num_of_products, 1)

        Ecommerce.get_instance().add_new_product('ofek', 'mystery book2', 50, 17, 'reading', store_number,
                                                 ['mystery', 'leisure'], 1, 70, 13)

        num_of_products = SQLHandler.get_instance().select_from_db('select count(*) from products')[0][0]
        self.assertEqual(num_of_products, 2)

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
