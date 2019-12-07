from src.db.sql_handler import SQLHandler
from src.message_response import MessageResponse

SQL = SQLHandler.get_instance()


def create_new_user_db(user_name, password, age):
    op = "INSERT INTO dbo.users VALUES ('" + user_name + "',HASHBYTES('SHA2_512','" + str(password) + "')," + \
         str(age) + ")"
    try:
        SQL.update(op)
        return MessageResponse(True, 1, "New user registered to the system")
    except Exception as e:
        return MessageResponse(False, 0, "The username already exists in the system")


def get_states(username):
    get = "select distinct state_id from [dbo].[user_rules] where username='" + username + "'"
    try:
        get = SQL.select_from_db(get)
        return MessageResponse(get, 1, "The states received successfully")
    except Exception as e:
        return MessageResponse(None, 0, "THe states cannot received")


def authentication_db(user_name, password):
    op = "SELECT * FROM dbo.users WHERE " \
         "USERNAME = '" + user_name + "' and password=HASHBYTES('SHA2_512','" + password + "')"
    try:
        result = SQL.select_from_db(op)
        if len(result) == 1:
            return MessageResponse(True, 1, "The authentication is succeeded")
        else:
            return MessageResponse(False, 1, "The authentication is failed")
    except Exception as e:
        return MessageResponse(False, 0, "Some details are wrong")


def add_manager_db(username_appoints, username_appointed, store_number):
    get_manager = "select * from dbo.user_rules where username='" + username_appoints + "' and store_number=" + \
                  str(store_number)
    insert_manager = "INSERT INTO dbo.user_rules VALUES ('" + username_appointed + "','" + str(store_number) + "','" + \
                     str(3) + "','" + username_appoints + "')"
    try:
        get_manager = SQL.select_from_db(get_manager)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot find appoints username")

    if len(get_manager) == 1:
        try:
            SQL.update(insert_manager)
            return MessageResponse(True,1, "New manager was added to the store")
        except Exception as e:
            return MessageResponse(False, 0, "Cannot add this manager")
    return MessageResponse(False, 1, "Cannot add this username to the store's managers")


def add_owner_db(username_appoints, username_appointed, store_number):
    get_owner = "select * from dbo.user_rules where username='" + username_appoints + "' and store_number=" + \
                str(store_number)
    insert_owner = "INSERT INTO dbo.user_rules VALUES ('" + username_appointed + "','" + str(store_number) + "','" + \
                   str(4) + "','" + username_appoints + "')"
    try:
        get_owner = SQL.select_from_db(get_owner)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot find appoints username")
    if len(get_owner) == 1:
        try:
            SQL.update(insert_owner)
            return MessageResponse(True, 1, "New owner was added to the store")
        except Exception as e:
            return MessageResponse(False, 0, "Cannot add this owner")
    return MessageResponse(False, 1, "Cannot add this username to the store's owners")


def open_new_store_db(name, supervisor_username, account_number, minimum_products, maximum_products, minimum_age):
    # need to check why you cannot open store, because of its name ?
    create_store = "INSERT INTO [dbo].[stores] ([name], [supervisor_username], [account_number], [minimum_products]" \
                   ", [maximum_products], [minimum_age]) VALUES ('" + name + "','" + supervisor_username + "'," + \
                   str(account_number) + "," + str(minimum_products) + "," + str(maximum_products) + "," \
                   + str(minimum_age) + ")  "
    scope = "DECLARE @scope int SET @scope = CAST(SCOPE_IDENTITY() as int)  "
    rules = " INSERT INTO [dbo].[user_rules] values ('" + supervisor_username + "',@scope," + str(4) + \
            ",'" + supervisor_username + "')"
    final_insert = create_store + scope + rules
    try:
        SQL.update(final_insert)
        get = "select top(1) store_number from [dbo].[stores] order by store_number desc"
        get = SQL.select_from_db(get)
        return MessageResponse(get, 1, "New store: " + name + " was opened by the user: " + supervisor_username)
    except Exception as e:
        return MessageResponse(None, 0, "cannot open this store")


def create_new_product_db(name, price, amount, category, store_number, key_words, minimum_products, maximum_products,
                          minimum_age):
    create_product = "INSERT INTO [dbo].[products] ([name], [price], [category], [store_number], [amount] ," \
                     "[minimum_products], [maximum_products], [minimum_age]) VALUES ('" + name + "'," + str(price) + \
                     ",'" + category + "'," + str(store_number) + "," + str(amount) + "," + str(minimum_products) + \
                     "," + str(maximum_products) + "," + str(minimum_age) + ") "

    scope = "DECLARE @scope int SET @scope = CAST(SCOPE_IDENTITY() as int)  "
    create_key_word = ""
    for key_word in key_words:
        create_key_word += "INSERT INTO [dbo].[products_key_words] values (@scope, '" + key_word + "' )"
    final_create_product_sql = create_product + scope + create_key_word

    try:
        SQL.update(final_create_product_sql)
        return MessageResponse(True, 1, "The product added successfully")

    except Exception as e:
        return MessageResponse(False, 0, "Cannot add this new product to the system")


def get_stores_of_user_owner_db(username):
    get_stores = "select store_number from [dbo].[user_rules] where username='" + username + \
                 "' and state_id=(select state_id from [dbo].[states] where state='STORE_OWNER')"
    try:
        get_stores = SQL.select_from_db(get_stores)
        return MessageResponse(get_stores, 1, "Successful retrieval of stores")
    except Exception as e:
        return MessageResponse(None, 0, "Cannot retrieve data about stores")


def get_stores_of_user_manager_db(username):
    get_stores = "select store_number from [dbo].[user_rules] where username='" + username + \
                 "' and state_id=(select state_id from [dbo].[states] where state='STORE_MANAGER')"
    try:
        get_stores = SQL.select_from_db(get_stores)
        return MessageResponse(get_stores, 1, "Successful retrieval of stores")
    except Exception as e:
        return MessageResponse(None, 0, "Cannot retrieve data about stores")


def search_products_by_category_db(category):
    get_products = " select * from [dbo].[products] as p join [dbo].[stores] as s " \
                   "on p.store_number=s.store_number where p.category='" + category + "' and s.is_enable=1"
    try:
        get_products = SQL.select_from_db(get_products)
        return MessageResponse(get_products, 1, "Successful retrieval of products")
    except Exception as e:
        return MessageResponse(None, 0, "Cannot retrieve data about products")


def search_products_by_name_db(name):
    get_products = " select p.catalog_number, p.name, p.price, p.category, p.store_number, p.amount, " \
                   "p.minimum_products, p.maximum_products, p.minimum_age from [dbo].[products] as p join " \
                   "[dbo].[stores] as s on p.store_number=s.store_number where p.name='" + name + "' and s.is_enable=1"
    try:
        get_products = SQL.select_from_db(get_products)
        return MessageResponse(get_products, 1, "Successful retrieval of products")
    except Exception as e:
        return MessageResponse(None, 0, "Cannot retrieve data about products")


def search_products_by_key_word_db(key_word):
    get_products = " select * from [dbo].[products_key_words] as k join [dbo].[products] as p " \
                   "on k.catalog_number=p.catalog_number join [dbo].[stores] as s on p.store_number=s.store_number " \
                   "where key_word='" + key_word + "' and s.is_enable=1"
    try:
        get_products = SQL.select_from_db(get_products)
        return MessageResponse(get_products, 1, "Successful retrieval of products")
    except Exception as e:
        return MessageResponse(None, 0, "Cannot retrieve data about products")


def get_product(catalog_number):
    get_p = " select * from [dbo].[products] where catalog_number = " + str(catalog_number)
    try:
        get_p = SQL.select_from_db(get_p)
        return MessageResponse(get_p, 1, "Successful retrieval of product with this catalog number")
    except Exception as e:
        return MessageResponse(None, 0, "Cannot retrieve data about product with this catalog number")


def is_the_store_open(store_number):
    is_enable = "select is_enable from [dbo].[stores] where store_number=" + str(store_number)
    is_enable = SQL.select_from_db(is_enable)
    return is_enable[0][0] == 1


def get_price_db(catalog_number):
    get_price = "select price from [dbo].[products] where catalog_number=" + str(catalog_number)
    get_price = SQL.select_from_db(get_price)
    return get_price[0][0]


def add_to_cart_db(username, catalog_number, cart):
    get_store_number = "select store_number from [dbo].[products] where catalog_number=" + str(catalog_number)
    try:
        get_store_number = SQL.select_from_db(get_store_number)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot get the store number of the product")
    if len(get_store_number) == 0:
        return MessageResponse(False, 1, "The product is not available")
    if not is_the_store_open(get_store_number[0][0]):
        return MessageResponse(False, 1, "The store that sells this product is not available")

    if cart is not None:  # case of guest
        return 1

    check = "select * from [dbo].[shopping_carts] where username='" + username + "' and catalog_number=" + \
            str(catalog_number)
    try:
        check = SQL.select_from_db(check)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot retrieve data about shopping cart")

    if len(check) == 1:  # needs to update the amount's field
        try:
            update_amount = " UPDATE [dbo].[shopping_carts] SET amount = (select amount from [dbo].[shopping_carts] " \
                            "where username ='" + username + "' and catalog_number=" + str(catalog_number) + ") + 1" \
                            "where catalog_number=" + str(catalog_number)
            SQL.update(update_amount)
            return MessageResponse(True, 1, "The amount of this product increment successfully")
        except Exception as e:
            return MessageResponse(False, 0, "Cannot increment product's amount")

    insert_to_cart = " INSERT INTO [dbo].[shopping_carts] VALUES ('" + username + "', " + str(catalog_number) + \
                     ", 1, " + "(select price from [dbo].[products] where catalog_number=" + str(catalog_number) + "))"
    try:
        SQL.update(insert_to_cart)
        return MessageResponse(True, 1, "New product was added to cart successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot add a new product to the cart")


def remove_from_cart_db(username, catalog_number):
    check_amount = "select amount from [dbo].[shopping_carts] where username='" + username + "' and catalog_number=" + \
            str(catalog_number)
    try:
        check_amount = SQL.select_from_db(check_amount)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot retrieve data about shopping cart")
    if len(check_amount) == 1 and check_amount[0][0] > 1:  # needs to dec the amount
        try:
            update_amount = " UPDATE [dbo].[shopping_carts] SET amount = (select amount from [dbo].[shopping_carts] " \
                            "where username ='" + username + "' and catalog_number=" + str(catalog_number) + ") - 1" \
                            "where catalog_number=" + str(catalog_number)
            SQL.update(update_amount)
            return MessageResponse(True, 1, "The amount of this product decrement successfully")
        except Exception as e:
            return MessageResponse(False, 0, "Cannot decrement product's amount")

    delete_from_cart = "Delete from [dbo].[shopping_carts] where username='" + username + "' and catalog_number=" + \
                       str(catalog_number)
    try:
        SQL.update(delete_from_cart)
        return MessageResponse(True, 1, "The product was removed from cart successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot remove a new product from the cart")


def show_store_db(store_number):
    get_store = 'select * from [dbo].[stores] where store_number=' + str(store_number)
    try:
        get_store = SQL.select_from_db(get_store)
    except Exception as e:
        return MessageResponse(None, 0, "Cannot retrieve data about this store")
    return MessageResponse(get_store, 1, "Successful retrieval of store")


def show_cart_db(username, store_number):
    get_products = "select sh.catalog_number, sh.amount, sh.price_per_product, p.name " \
                   "from [dbo].[shopping_carts] as sh join [dbo].[products] as p " \
                   "on sh.catalog_number=p.catalog_number where username='" + username + \
                   "' and exists (select catalog_number from [dbo].[products] " \
                   "where catalog_number = sh.catalog_number and store_number=" + str(store_number) + ")"
    try:
        get_products = SQL.select_from_db(get_products)
        return MessageResponse(get_products, 1, "Successful retrieval of shopping cart")
    except Exception as e:
        return MessageResponse(None, 0, "Cannot retrieve data about shopping cart")


def close_permanently_db(username, store_number):
    check_if_admin = "select username from [dbo].[user_rules] where state_id=2 and username='" + username + "'"

    try:
        check_if_admin = SQL.select_from_db(check_if_admin)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot retrieve data about Admin")

    if len(check_if_admin) == 0:
        return MessageResponse(True, 1, "The username isn't an Admin so he cannot close the store permanently")

    delete_store = "delete from [dbo].[cond_discount] where exists (select catalog_number " \
                   "from [dbo].[products] as t where store_number =" + str(store_number) + " and t.catalog_number = " \
                                                                                           "catalog_number) " \
                   "delete from [dbo].[coupon_discount] where exists (select catalog_number " \
                   "from [dbo].[products] as t where store_number =" + str(store_number) + " and t.catalog_number = " \
                                                                                           "catalog_number) " \
                   "delete from [dbo].[products_key_words] where exists (select catalog_number " \
                   "from [dbo].[products] as t where store_number =" + str(store_number) + " and t.catalog_number = " \
                                                                                           "catalog_number) " \
                   "delete from [dbo].[reg_discount] where exists (select catalog_number " \
                   "from [dbo].[products] as t where store_number =" + str(store_number) + " and t.catalog_number = " \
                                                                                           "catalog_number) " \
                   "delete from [dbo].[shopping_carts] where exists (select catalog_number " \
                   "from [dbo].[products] as t where store_number =" + str(store_number) + " and t.catalog_number = " \
                                                                                           "catalog_number) " \
                   "delete from [dbo].[products] where store_number =" + str(store_number) + " "\
                   "delete from [dbo].[user_rules] where store_number =" + str(store_number) + " " \
                   "delete from [dbo].[stores] where store_number =" + str(store_number)
    try:
        SQL.update(delete_store)
        return MessageResponse(True, 1, "The Store was Closed permanently")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot close this store permanently")


def inc_product_amount_db(catalog_number, amount):
    update_amount = "Update [dbo].[products] SET amount = (select amount from [dbo].[products]" \
                    "where catalog_number=" + str(catalog_number) + ") + " + str(amount) + "where catalog_number=" + \
                    str(catalog_number)
    try:
        SQL.update(update_amount)
        return MessageResponse(True, 1, "The amount was increased successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot increase the amount")


def dec_product_amount_db(catalog_number, amount):
    update_amount = "Update [dbo].[products] SET amount = (select amount from [dbo].[products]" \
                    "where catalog_number=" + str(catalog_number) + ") - " + str(amount) + "where catalog_number=" + \
                    str(catalog_number)
    try:
        SQL.update(update_amount)
        return MessageResponse(True, 1, "The amount was decreased successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot decrease the amount")


def remove_product_from_store_db(catalog_number):
    delete_store = "delete from [dbo].[cond_discount]  where catalog_number =" + str(catalog_number) + \
               " delete from [dbo].[coupon_discount] where catalog_number =" + str(catalog_number) + \
               " delete from [dbo].[products_key_words] where catalog_number =" + str(catalog_number) + \
               " delete from [dbo].[reg_discount] where catalog_number =" + str(catalog_number) + \
               " delete from [dbo].[shopping_carts] where catalog_number =" + str(catalog_number) + \
               " delete from [dbo].[products] where catalog_number =" + str(catalog_number)
    try:
        SQL.update(delete_store)
        return MessageResponse(True, 1, "The product was removed successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot remove this product")


def is_in_rule_in_the_store_db(username, rule, store_number):
    check_if_in_rule = "select username from [dbo].[user_rules] where username='" + username + \
                       "' and store_number=" + str(store_number) + "and state_id=" \
                       "(select state_id from [dbo].[states] where state='" + rule + "')"
    try:
        check_if_in_rule = SQL.select_from_db(check_if_in_rule)
        return len(check_if_in_rule) == 1
    except Exception as e:
        return MessageResponse(False, 0, "Cannot retrieve data about the username")


def can_the_user_remove_him(username, store_number, appointed_username):
    appointed = appointed_username
    while 1:
        appoint_username = "select appoint_username from [dbo].[user_rules] where username='" + \
                           appointed + "' and store_number=" + str(store_number)
        try:
            appoint_username = SQL.select_from_db(appoint_username)
        except Exception as e:
            return MessageResponse(False, "Cannot retrieve data about the username")
        if appoint_username[0][0] == appointed:
            return MessageResponse(True, "The username cannot remove this owner")
        if appoint_username[0][0] == username:
            return True
        appointed = appoint_username[0][0]


def remove_store_owner_db(username, store_number, appointed_username):
    check_if_in_owner = is_in_rule_in_the_store_db(appointed_username, "STORE_OWNER", store_number)
    if (check_if_in_owner is not True) and (check_if_in_owner is not False):
        return check_if_in_owner
    elif check_if_in_owner is False:
        return MessageResponse(False, 1, "The appointed username is'nt an owner of this store")
    can_the_user_remove_the_owner = can_the_user_remove_him(username, store_number, appointed_username)
    if can_the_user_remove_the_owner is not True:
        return can_the_user_remove_the_owner
    delete_appointed_username = "delete from [dbo].[user_rules] where username='" + appointed_username + \
                                "' and store_number=" + str(store_number)
    try:
        SQL.update(delete_appointed_username)
        return MessageResponse(True, 1, "This owner was removed successfully")
    except Exception as e:
        return MessageResponse(False, 0, "The deletion failed")


def remove_store_manager_db(username, store_number, appointed_username):
    check_if_in_manager = is_in_rule_in_the_store_db(appointed_username, "STORE_MANAGER", store_number)
    if (check_if_in_manager is not True) and (check_if_in_manager is not False):
        return check_if_in_manager
    elif check_if_in_manager is False:
        return MessageResponse(False, 1, "The appointed username is'nt a manager of this store")
    can_the_user_remove_the_manager = can_the_user_remove_him(username, store_number, appointed_username)
    if can_the_user_remove_the_manager is not True:
        return can_the_user_remove_the_manager
    delete_appointed_username = "delete from [dbo].[user_rules] where username='" + appointed_username + \
                                "' and store_number=" + str(store_number)
    try:
        SQL.update(delete_appointed_username)
        return MessageResponse(True, 1, "This manager was removed successfully")
    except Exception as e:
        return MessageResponse(False, 0, "The deletion failed")


def close_store_db(username, store_number):
    check_if_user_with_rule = "select username from [dbo].[user_rules] where store_number=" + str(store_number) + \
                              " and username='" + username + "'"
    try:
        check_if_user_with_rule = SQL.select_from_db(check_if_user_with_rule)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot retrieve data about the username")
    if len(check_if_user_with_rule) == 0:
        return MessageResponse(False, 1, "The user isn't an owner or manager of this store")
    check_if_close = "select is_enable from [dbo].[stores] where is_enable=0"
    try:
        check_if_close = SQL.select_from_db(check_if_close)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot retrieve data about the store")
    if len(check_if_close) != 0:
        return MessageResponse(False, 1, "The store is already close")
    update_store_state = "update [dbo].[stores] set is_enable=0 where store_number=" + str(store_number)
    delete_from_cart = "delete from [dbo].[shopping_carts] where exists " \
                       "(select catalog_number from [dbo].[products] as p where p.catalog_number=catalog_number " \
                       "and p.store_number=" + str(store_number) + ")"
    try:
        SQL.update(update_store_state)
        SQL.update(delete_from_cart)
        return MessageResponse(True, 1, "The store was closed successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Problems with the close of the store")


def get_store_number_by_product_db(catalog_number):
    get_store_number = "select store_number from [dbo].[products] where catalog_number=" + str(catalog_number)
    try:
        get_store_number = SQL.select_from_db(get_store_number)
        return get_store_number[0][0]
    except Exception as e:
        return False


def create_new_admin_db(username, password, age):
    create_new_user_db(username, password, age)
    make_admin = "insert into [dbo].[user_rules] values('" + username + "', null, 2, '" + username + "')"
    try:
        SQL.update(make_admin)
        return MessageResponse(True, 1, "New admin was created")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot create new admin")
        return MessageResponse(False, 0, "Cannot create new admin")


def remove_subscriber_db(username, user_to_remove):
    check_username_of_admin = "select username from [dbo].[user_rules] where username='" + username + "' and state_id=2"
    try:
        check_username_of_admin = SQL.select_from_db(check_username_of_admin)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot get this username")
    if len(check_username_of_admin) == 0:
        return MessageResponse(True, 1, "This username is not an Admin")
    delete_user = "delete from [dbo].[user_rules] where username='" + user_to_remove + "' " + \
                  "delete from [dbo].[shopping_carts] where username='" + user_to_remove + "' " + \
                  "delete [dbo].[users] where username='" + user_to_remove + "' "
    try:
        SQL.update(delete_user)
        return MessageResponse(True, 1, "The user removed successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot remove this user")


def change_details_of_product_db(catalog_number, attribute, value):
    update_product = "update [dbo].[products] set " + attribute + "=" + str(value) + "where catalog_number=" + \
                     str(catalog_number)
    try:
        SQL.update(update_product)
        return MessageResponse(True, 1, "Product's detail was changed successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot update the filed of product")


def change_details_of_store_db(store_number, attribute, value):
    update_store = "update [dbo].[stores] set " + attribute + "=" + str(value) + "where store_number=" + \
                     str(store_number)
    try:
        SQL.update(update_store)
        return MessageResponse(True, 1, "Store's detail was changed successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot update the filed of store")


def get_all_stores_db():
    get_stores = "select store_number from [dbo].[stores]"
    return SQL.select_from_db(get_stores)


def get_detail_of_store_db(store_number, detail):
    get = "select " + detail + " from [dbo].[stores] where store_number=" + str(store_number)
    get = SQL.select_from_db(get)
    return get[0][0]


def get_detail_of_product_db(catalog_number, detail):
    get = "select " + detail + " from [dbo].[products] where catalog_number=" + str(catalog_number)
    get = SQL.select_from_db(get)
    return get[0][0]


def get_age_of_user_db(username):
    get = "select age from [dbo].[users] where username='" + username + "'"
    get = SQL.select_from_db(get)
    return get[0][0]


def get_reg_discount_of_product_db(catalog_number):
    get = "select * from [dbo].[reg_discount] where catalog_number=" + str(catalog_number)
    get = SQL.select_from_db(get)
    if len(get) == 0:
        return False
    else:
        return get[0]


def get_cond_discount_of_product_db(catalog_number):
    get = "select * from [dbo].[cond_discount] where catalog_number=" + str(catalog_number)
    get = SQL.select_from_db(get)
    if len(get) == 0:
        return False
    else:
        return get[0]


def get_coupon_discount_of_product_db(catalog_number):
    get = "select * from [dbo].[coupon_discount] where catalog_number=" + str(catalog_number)
    get = SQL.select_from_db(get)
    if len(get) == 0:
        return False
    else:
        return get[0]


def get_reg_discount_of_store_db(store_number):
    get = "select * from [dbo].[store_discount] where store_number=" + str(store_number)
    get = SQL.select_from_db(get)
    if len(get) == 0:
        return False
    else:
        return get[0]


def remove_all_carts(username):
    delete_cart = "delete from [dbo].[shopping_carts] where username='" + username + "'"
    try:
        SQL.update(delete_cart)
        return MessageResponse(True, 1, "All carts of the user were removed")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot remove all carts")


def reopen_store_db(username, store_number):
    check_if_user_with_rule = "select username from [dbo].[user_rules] where store_number=" + str(store_number) + \
                              " and username='" + username + "'"
    try:
        check_if_user_with_rule = SQL.select_from_db(check_if_user_with_rule)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot retrieve data about the username")
    if len(check_if_user_with_rule) == 0:
        return MessageResponse(False, 1, "The user isn't an owner or manager of this store")
    check_if_open = "select is_enable from [dbo].[stores] where is_enable=1"
    try:
        check_if_open = SQL.select_from_db(check_if_open)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot retrieve data about the store")
    if len(check_if_open) != 0:
        return MessageResponse(False, 1, "The store is already open")
    update_store_state = "update [dbo].[stores] set is_enable=1 where store_number=" + str(store_number)
    try:
        SQL.update(update_store_state)
        return MessageResponse(True, 1, "The store was reopen successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Problems with the opening of the store")


def get_products_of_store(store_number):
    get = "select * from [dbo].[stores] where store_number=" + str(store_number)
    try:
        return SQL.select_from_db(get)
    except Exception as e:
        return False


def add_reg_discount__of_store_db(store_number, discount_percentages, double_deals, start_time, end_time):
    delete_reg_discount = "delete from [dbo].[store_discount] where catalog_number=" + str(store_number)
    insert_reg_discount = "insert into [dbo].[store_discount] values(" + str(store_number) + ", " + \
                             str(discount_percentages) + "," + str(double_deals) + ", '" + \
                             start_time + "', '" + end_time + "')"
    try:
        SQL.update(delete_reg_discount)
        SQL.update(insert_reg_discount)
        return MessageResponse(True, 1, "The regular discount added successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot add this regular discount")


def add_reg_discount_db(catalog_number, discount_percentages, double_deals, start_time, end_time):
    delete_reg_discount = "delete from [dbo].[reg_discount] where catalog_number=" + str(catalog_number)
    insert_reg_discount = "insert into [dbo].[reg_discount] values(" + str(catalog_number) + ", " + \
                          str(discount_percentages) + ", " + str(double_deals) + ", '" + \
                          start_time + "', '" + end_time + "')"
    try:
        SQL.update(delete_reg_discount)
        SQL.update(insert_reg_discount)
        return MessageResponse(True, 1, "The regular discount added successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot add this regular discount")


def add_cond_discount_db(catalog_number, discount_percentages, double_deals, start_time, end_time,
                         conditional_type, catalog_number_of_second_product):
    delete_cond_discount = "delete from [dbo].[cond_discount] where catalog_number=" + str(catalog_number)
    insert_cond_discount = "insert into [dbo].[cond_discount] values(" + str(catalog_number) + ", " + \
                           str(discount_percentages) + "," + str(double_deals) + \
                           ", '" + start_time + "', '" + end_time + "', '" + conditional_type + "', " + \
                           str(catalog_number_of_second_product) + ")"
    try:
        SQL.update(delete_cond_discount)
        SQL.update(insert_cond_discount)
        return MessageResponse(True, 1, "The conditional discount added successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot add this conditional discount")


def add_coupon_discount_db(catalog_number, discount_percentages, double_deals, start_time, end_time):
    delete_coupon_discount = "delete from [dbo].[coupon_discount] where catalog_number=" + str(catalog_number)
    insert_coupon_discount = "insert into [dbo].[coupon_discount] values(" + str(catalog_number) + ", " + \
                             str(discount_percentages) + "," + str(double_deals) + ", '" + \
                             start_time + "', '" + end_time + "')"
    try:
        SQL.update(delete_coupon_discount)
        SQL.update(insert_coupon_discount)
        return MessageResponse(True, 1, "The coupon discount added successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot add this coupon discount")


def is_product_in_store_db(self, store_number, catalog_number):
    there_is_store = show_store_db(store_number)
    if there_is_store.val is None:
        return there_is_store
    if len(there_is_store.val) == 0:
        return MessageResponse(False, 1, "There is no such store in the system")
    there_is_product_in_store = 'select * from [dbo].[products] where store_number=' + str(store_number) + \
                                ' and catalog_number=' + str(catalog_number)
    try:
        there_is_product_in_store = SQL.select_from_db(there_is_product_in_store)
    except Exception as e:
        return MessageResponse(False, 0, "Cannot get this details about store_number and product")
    if len(there_is_product_in_store) == 0:
        return MessageResponse(False, 1, "There is no such product in the store")
    return MessageResponse(True, 1, "The product is exist in the store")


def empty_tables():
    delete_tables_query ="delete from [dbo].[cond_discount] ; delete from  [dbo].[coupon_discount];" \
                         " delete from [dbo].[reg_discount] ; delete from [dbo].[products_key_words];" \
                         " delete from [dbo].[shopping_carts]; delete from [dbo].[user_rules];" \
                         " delete from [dbo].[products]; delete from [dbo].[stores]; delete from [dbo].[users];"
    try:
        SQL.update(delete_tables_query)
        return MessageResponse(True, 1, "deleted tables successfully")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot delete tables")


def drop_users():
    delete_tables_query = "delete from [dbo].[products];  delete from [dbo].[stores]; delete from [dbo].users; "
    try:
        SQL.update(delete_tables_query)
        return MessageResponse(True, 1, "deleted user table")
    except Exception as e:
        return MessageResponse(False, 0, "Cannot delete user table")

