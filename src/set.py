from src.ecommerce import Ecommerce
import json
import os
from src.db.db_functions import empty_tables


class Setting:

    @staticmethod
    def setup():
        Setting.initilize_json()
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../data.txt")
        stores_opend = []
        with open(path) as json_file:
            data = json.load(json_file)
            for p in data['usecases']:
                if p['action'] == 'login':
                    print(Ecommerce.get_instance().login(p['username'], p['password']).message)
                elif p['action'] == 'guest-registration':
                    # print(Ecommerce.get_instance().register(p['username'], p['password'], p['age']).val)
                    print(Ecommerce.get_instance().register(p['username'], p['password'], p['age']).message)
                elif p['action'] == 'search-product':
                    print(Ecommerce.get_instance().search_product(p['attribute'], p['value']).message)
                elif p['action'] == 'add-product-to-basket':
                    print(Ecommerce.get_instance().add_new_product(p['store_number'], p['name'], p['price'],
                                                                   p['category'], p['key_words']).message)
                elif p['action'] == 'open-store':
                    store_open_response = Ecommerce.get_instance().open_new_store(p['store_name'], p['username'],
                                                                  p['account_number'],
                                                                  p['minimum_products'],
                                                                  p['maximum_products'],
                                                                  p['minimum_age'])
                    stores_opend.append({"username": p['username'], "store_name": p['store_name'],
                                         "store_number": store_open_response.val[0][0]})
                    print(store_open_response.message)
                    # print("bbb ", store_open_response.val[0][0])
                elif p['action'] == 'add-product-to-store':
                    store_number_found = -1
                    for storeli in stores_opend:
                        if p['username'] == storeli["username"] and p['store_name'] == storeli["store_name"]:
                            store_number_found = storeli["store_number"]
                            print(store_number_found)
                    if store_number_found == -1:
                        print('failed found store number')
                    else:
                        print(Ecommerce.get_instance().add_new_product(p['username'], p['product_name'],
                                                                       int(p['price']),
                                                                       int(p['quantity']), p['category'],
                                                                       store_number_found,
                                                                       p['key_words'], p['minimum_products'],
                                                                       p['maximum_products'], p['minimum_age']).message)
                elif p['action'] == 'remove-product-from-store':
                    print(Ecommerce.get_instance().remove_product(p['username'],
                                                                  p['product_catalog_number']).message)
                elif p['action'] == 'remove-subscriber':
                    print(Ecommerce.get_instance().remove_subscriber(p['username'], p['username_to_remove']).message)
                elif p['action'] == 'make-admin':
                    print(Ecommerce.get_instance().make_admin(p['username'], p['password'], 22).message)
                elif p['action'] == 'appoint-store-owner':
                    store_number_found = -1
                    for storeli in stores_opend:
                        if p['username'] == storeli["username"] and p['store_name'] == storeli["store_name"]:
                            store_number_found = storeli["store_number"]
                    if store_number_found == -1:
                        print('failed found store number')
                    else:
                        print(Ecommerce.get_instance().add_store_manager(p['username'], store_number_found,
                                                                         p['candidate_user']).message)
                elif p['action'] == 'appoint-manager':
                    store_number_found = -1
                    for storeli in stores_opend:
                        if p['username'] == storeli["username"] and p['store_name'] == storeli["store_name"]:
                            store_number_found = storeli["store_number"]
                            print(store_number_found)
                    if store_number_found == -1:
                        print('failed found store number')
                    else:
                        print(Ecommerce.get_instance().add_store_manager( p['username'], store_number_found,
                                                                          p['candidate_user']).message)

    @staticmethod
    def startup():
        print(Ecommerce.get_instance().make_admin("admin", "12345678", 24).message)
        Setting.setup()

    @staticmethod
    def initilize_json():
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "../data.txt")
        data = {'usecases': []}

        data['usecases'].append({
            'action': 'make-admin',
            'username': 'A1',
            'password': '12345678'
        })
        data['usecases'].append({
            'action': 'guest-registration',
            'username': 'U1',
            'password': '12345678',
            'age': '24'
        })
        data['usecases'].append({
            'action': 'guest-registration',
            'username': 'U2',
            'password': '12345678',
            'age': '18'
        })
        data['usecases'].append({
            'action': 'guest-registration',
            'username': 'U11',
            'password': '12345678',
            'age': '27'
        })
        data['usecases'].append({
            'action': 'guest-registration',
            'username': 'U12',
            'password': '12345678',
            'age': '33'
        })
        data['usecases'].append({
            'action': 'guest-registration',
            'username': 'U13',
            'password': '12345678',
            'age': '33'
        })
        data['usecases'].append({
            'action': 'open-store',
            'username': 'U11',
            'store_name': "S2",
            'account_number': "12344",
            'minimum_products': '0',
            'maximum_products': '1000',
            'minimum_age': '-1'
        })

        with open(path, 'w') as outfile:
            json.dump(data, outfile)




        #
        # #
        # # # make u1 admin
        # data['usecases'].append({
        #     'action': 'make-admin',
        #     'username': 'u1',
        #     'password': 'u112345678'
        # })
        # # #
        # # # u2 opens store s1 , need login before
        # data['usecases'].append({
        #     'action': 'login',
        #     'username': 'u2',
        #     'password': 'u212345678',
        # })
        # data['usecases'].append({
        #     'action': 'open-store',
        #     'username': 'u2',
        #     'store_name': "s1",
        #     'account_number': "12344",
        #     'minimum_products': '0',
        #     'maximum_products': '100',
        #     'minimum_age': '16'
        # })
        # #
        # # # u2 adds item “diapers” to store s1 with cost 30 and quantity 20
        # data['usecases'].append({
        #     'action': 'add-product-to-store',
        #     'username': 'u2',
        #     'password': 'u212345678',
        #     'store_name': 's1',
        #     'product_name': 'diapers',
        #     'price': '30',
        #     'quantity': '20',
        #     'category': 'babies',
        #     'key_words': 'poo',
        #     'minimum_products': '1',
        #     'maximum_products': '12',
        #     'minimum_age': 0
        # })
        # #
        # # # u2 appoints u3 to a store manager of store s1 with the permission to manage inventory.
        # data['usecases'].append({
        #     'action': 'appoint-manager',
        #     'username': 'u2',
        #     'password': 'u212345678',
        #     'store_name': 's1',
        #     'candidate_user': 'u3',
        #     'permissions': 'manage-inventory',
        # })
        # data['usecases'].append({
        #     'action': 'remove-subscriber',
        #     'username': 'u3',
        #     'username_to_remove': 'u1'
        # })
        # data['usecases'].append({
        #     'action': 'appoint-store-owner',
        #     'username': 'u2',
        #     'candidate_user': 'u3',
        #     'store_name': 's1',
        # })

