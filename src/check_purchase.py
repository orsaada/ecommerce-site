import datetime
from src.ecommerce import Ecommerce
from src.delivery_system import DeliveryAddress
# from src.db.db_functions import *

# x = Ecommerce.get_instance().open_new_store('check', 'ofek', 123, 0, 10, 0) 27
# x = Ecommerce.get_instance().add_new_product('ofek', 'banana', 10, 10, 'fruit', 27, [], 0, 10, 0)
x = Ecommerce.get_instance().add_reg_discount('ofek', 25, 32, 1, '2018-06-20', '2019-06-21')
# x = Ecommerce.get_instance().add_cond_discount('ofek', 21, 30, 1, '2018-07-25', '2028-07-25', 'or', 27)
# x = Ecommerce.get_instance().change_details_of_product('ofek', 27, 'maximum_products', 1000)
x = Ecommerce.get_instance().change_details_of_store('ofek', 9, 'maximum_products', 1000)
x = Ecommerce.get_instance().change_details_of_product('ofek', 25, 'maximum_products', 1000)
x = Ecommerce.get_instance().change_details_of_product('ofek', 25, 'Amount', 100)
x = Ecommerce.get_instance().add_to_cart('ofek', 25, None)
# x = Ecommerce.get_instance().change_details_of_product('ofek', 18, 'maximum_products', 1000)
# x = Ecommerce.get_instance().change_details_of_product('ofek', 18, 'Amount', 100)
# x = Ecommerce.get_instance().add_to_cart('ofek', 18, None)
# x = Ecommerce.get_instance().add_to_cart('ofek', 18, None)
x = Ecommerce.get_instance().make_purchase('ofek', '124', ['12345676543', 'ofek', '333', '07', '12'],
                                           DeliveryAddress(5, 'Israel'), None, None)

# # x = get_price_db(12)
print('x:', x.val[0].__dict__)

