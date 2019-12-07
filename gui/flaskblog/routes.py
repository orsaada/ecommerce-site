from flask import render_template, url_for, flash, redirect, request, session
from gui.flaskblog import app
from gui.flaskblog.forms import (LoginForm, SearchForm, PurchaseForm, NewProductForm,
                                 UpdateDetailsForm, NewStoreForm, RemoveFromCartForm, AddToCartForm, RemoveSubscriberForm,
                                 RemoveProductForm, CartManagementForm,
                                 ShowStoreForm, CloseStoreForm, AddRegularDiscountPolicyToProduct,
                                 AddConditionalDiscountPolicyToProduct, AddDiscountPolicyToStore, PermanentlyClose,
                                 LimitQuantity, LimitAge, LimitQuantityPerStore,
                                 ShowCartForm, RegistrationForm, AddBuyingPolicyForm, AddDiscountPolicyForm,
                                 ProductManagementForm, PoliciesForm, AdminOptionsForm, WorkersManagementForm,
                                 AddStoreManager, AddStoreOwner, RemoveStoreManager, RemoveStoreOwner)
from src.state import State
from src.ecommerce import Ecommerce
from src import delivery_system


class TempUser:
    def __init__(self, user_id, username, states, shopping_basket):
        self.user_id = user_id
        self.username = username
        self.states = states
        self.shopping_basket = shopping_basket
        self.is_logged_in = False


class UserSessions:

    current_user = None
    counter = 0
    users = {}

    @staticmethod
    def add_user():
        session['user'] = UserSessions.counter
        UserSessions.users[UserSessions.counter] = TempUser(UserSessions.counter, 'guest', [], [])
        UserSessions.counter += 1

    @staticmethod
    def get_user(user_id: int):
        return UserSessions.users[user_id]

    @staticmethod
    def log_user_in(user_id: int, username: str, states):
        UserSessions.users[user_id].username = username
        UserSessions.users[user_id].states = states
        UserSessions.users[user_id].shopping_basket = None
        UserSessions.users[user_id].is_logged_in = True

    @staticmethod
    def log_user_out(user_id: int):
        UserSessions.users[user_id].username = 'guest'
        UserSessions.users[user_id].states = []
        UserSessions.users[user_id].shopping_basket = []
        UserSessions.users[user_id].is_logged_in = False


@app.context_processor
def context_processor():
    return dict(me=UserSessions.current_user, state=State)


@app.before_request
def before_request():
    if 'user' not in session:
        UserSessions.add_user()
    UserSessions.current_user = UserSessions.get_user(session['user'])


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        products = Ecommerce.get_instance().search_product(request.form.get('attribute'), form.value.data)
        if products.val is None:
            flash(products.message, 'danger')
            products.val = []
        return render_template('home.html', form=form, title='Search', legend='Search', products=products.val)
    return render_template('home.html', me=UserSessions.current_user, form=form, title='Search', legend='Search')


@app.route("/cart_management", methods=['GET', 'POST'])
def cart_management():
    form = CartManagementForm()
    if form.validate_on_submit():
        if form.submit0.data:
            return redirect(url_for('add_to_cart'))
        elif form.submit1.data:
            return redirect(url_for('remove_from_cart'))
    return render_template('cart_management.html', title='Cart Management',
                           legend='Please Choose An Option:', form=form)


@app.route("/add_to_cart", methods=['GET', 'POST'])
def add_to_cart():
    form = AddToCartForm()
    print('bbb')
    if form.validate_on_submit():
        print('aaaa')
        if UserSessions.current_user.is_logged_in:
            resp = Ecommerce.get_instance().add_to_cart(UserSessions.current_user.username,
                                                        form.catalog_number.data, None)
        else:
            check_if_store_exist = Ecommerce.get_instance().is_product_in_store(form.store_number.data,
                                                                                form.catalog_number.data)
            if check_if_store_exist.val:
                for shopping_cart in UserSessions.current_user.shopping_basket:
                    if form.store_number.data == shopping_cart['store_number']:
                        resp = Ecommerce.get_instance().add_to_cart(UserSessions.current_user.username,
                                                                         form.catalog_number.data, shopping_cart)
                    else:
                        new_cart = [{'store_number': form.store_number.data, 'products': []}]
                        UserSessions.current_user.shopping_basket.appent(new_cart)
                        resp = Ecommerce.get_instance().add_to_cart(UserSessions.current_user.username,
                                                                         form.catalog_number.data, new_cart)
            else:
                flash(check_if_store_exist.message, 'danger')
        # ADD ANOTHER FIELD BASED ON GUEST OR NOT!!!!!!!!!!!!!!!!!!
        # from UserSessions.current_user.shopping_basket!!!!!!!!!!!!!!!!!!!
        flash(resp.message, 'success' if resp.val else 'danger')
        return render_template('add_to_cart.html', form=form, title='Add To Cart', legend='Add To Cart',
                               is_logged_in=UserSessions.current_user.is_logged_in)
    return render_template('add_to_cart.html', form=form, title='Add To Cart', legend='Add To Cart',
                           is_logged_in=UserSessions.current_user.is_logged_in)


@app.route("/remove_from_cart", methods=['GET', 'POST'])
def remove_from_cart():
    form = RemoveFromCartForm()
    if form.validate_on_submit():
        if UserSessions.current_user.is_logged_in:
            resp = Ecommerce.get_instance().remove_from_cart(UserSessions.current_user.username,
                                                        form.catalog_number.data, None)
        else:
            check_if_store_exist = Ecommerce.get_instance().is_product_in_store(form.store_number.data, form.catalog_number.data)
            if check_if_store_exist.val:
                for shopping_cart in UserSessions.current_user.shopping_basket:
                    if form.store_number.data == shopping_cart['store_number']:
                        resp = Ecommerce.get_instance().remove_from_cart(UserSessions.current_user.username,
                                                                    form.catalog_number.data, shopping_cart)
            else:
                flash(check_if_store_exist.message, 'danger')
        flash(resp.message, 'success' if resp.val else 'danger')
        return render_template('remove_from_cart.html', form=form, title='Remove From Cart', legend='Remove From Cart',
                               is_logged_in=UserSessions.current_user.is_logged_in)
    return render_template('remove_from_cart.html', form=form, title='Remove From Cart', legend='Remove From Cart',
                           is_logged_in=UserSessions.current_user.is_logged_in)


@app.route("/basket", methods=['GET', 'POST'])
def basket():

    form = PurchaseForm()
    products = []
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print('amir')

        delivery_sys = delivery_system.DeliveryAddress(form.country.data, form.city.data, form.street.data,
                                                       form.zip.data)
        resp = Ecommerce.get_instance().make_purchase(UserSessions.current_user.username,
                                                      'credit card', [form.card_number.data, form.holder.data,
                                                                      form.cvv.data, form.month.data, form.year.data],
                                                      delivery_sys, None, None)
        if resp.val is not False:
            products = resp.val
        print('amir')
        flash(resp.message, 'success' if resp.val else 'danger')
        return render_template('basket.html', products=products, form=form, title='Basket', legend='Shopping Basket'
                               , is_logged_in=UserSessions.current_user.is_logged_in)
    print('ofek')
    return render_template('basket.html', products=products, form=form, title='Basket', legend='Shopping Basket',
                           is_logged_in=UserSessions.current_user.is_logged_in)


@app.route("/show_cart", methods=['GET', 'POST'])
def show_cart():
    form = ShowCartForm()
    if form.validate_on_submit():
        if UserSessions.current_user.is_logged_in:
            products = Ecommerce.get_instance().show_cart(UserSessions.current_user.username, form.store_number.data)
            message = products.message
            products = products.val
        else:
            products = []
            message = 'Could not find the shopping cart you were looking for'
            for shopping_cart in UserSessions.current_user.shopping_basket:
                if shopping_cart['store_number'] == form.store_number.data:
                    products = shopping_cart['products']
                    message = 'Found the shopping cart you were looking for'

        if products is None:
            flash(message, 'danger')
        elif len(products) == 0:
            flash('No products were found', 'danger')
        else:
            return render_template('show_cart.html', form=form, title='Show Cart', legend='Show Cart',
                                   products=products, store_number=form.store_number.data)
    return render_template('show_cart.html', form=form, title='Show Cart', legend='Show Cart')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().register(form.username.data, form.password.data, form.age.data)
        if not resp.val:
            flash(resp.message, 'danger')
        else:
            flash(resp.message, 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().login(form.username.data, form.password.data)
        if resp.val is None:
            flash('Login Unsuccessful. Please check username and password', 'danger')
        else:
            context_processor()
            states = []
            for element in resp.val:
                states.append(element[0])
            if len(states) == 0:
                states.append(1)        # subscriber
            UserSessions.log_user_in(UserSessions.current_user.user_id, form.username.data, states)
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():

    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    UserSessions.log_user_out(UserSessions.current_user.user_id)
    context_processor()
    return redirect(url_for('home'))


@app.route("/new_product", methods=['GET', 'POST'])
def new_product():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = NewProductForm()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().add_new_product(UserSessions.current_user.username, form.name.data,
                                                        form.price.data, form.amount.data, form.category.data,
                                                        form.store_number.data, form.keywords.data.split(), -1,
                                                        -1, 0)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('new_product'))
    return render_template('create_product.html', form=form, title='New Product', legend='New Product')


@app.route("/new_store", methods=['GET', 'POST'])
def new_store():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = NewStoreForm()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().open_new_store(form.store_name.data, UserSessions.current_user.username,
                                                       form.account_number.data,
                                                       -1, -1, 0)
        if resp.val is None:
            flash('Could not open store', 'danger')
        else:
            flash('Your new store number is '+str(resp.val[0][0]), 'success')

        return redirect(url_for('new_store'))
    return render_template('new_store.html', form=form, title='New Store', legend='New Store')


@app.route("/update_product_details", methods=['GET', 'POST'])
def update_product_details():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = UpdateDetailsForm()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().change_details_of_product(UserSessions.current_user.username,
                                                                  form.catalog_number.data,
                                                                  form.attribute.data, form.value.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('update_product_details'))
    return render_template('update_product_details.html', form=form, title='Update Product Details',
                           legend='Update Product Details')


@app.route("/remove_subscriber", methods=['GET', 'POST'])
def remove_subscriber():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = RemoveSubscriberForm()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().remove_subscriber(UserSessions.current_user.username, form.username.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('remove_subscriber'))
    return render_template('remove_subscriber.html', form=form, title='Remove Subscriber', legend='Remove Subscriber')


@app.route("/remove_product", methods=['GET', 'POST'])
def remove_product():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = RemoveProductForm()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().remove_product(UserSessions.current_user.username,
                                                       form.catalog_number.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('remove_product'))
    return render_template('remove_product.html', form=form, title='Remove Product', legend='Remove Product')


@app.route("/show_store", methods=['GET', 'POST'])
def show_store():
    form = ShowStoreForm()
    if form.validate_on_submit():
        products = Ecommerce.get_instance().show_store(form.store_number.data)
        if products.val is None:
            flash(products.message, 'danger')
            products.val = []
        return render_template('show_store.html', form=form, title='Search', legend='Search', products=products.val)
    return render_template('show_store.html', form=form, title='Show Store', legend='Show Store')


@app.route("/close_store", methods=['GET', 'POST'])
def close_store():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = CloseStoreForm()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().close_store(UserSessions.current_user.username, form.store_number.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('close_store'))
    return render_template('close_store.html', form=form, title='Close Store', legend='Close Store')


@app.route("/add_regular_discount", methods=['GET', 'POST'])
def add_regular_discount():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = AddRegularDiscountPolicyToProduct()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().add_reg_discount( UserSessions.current_user.username,form.catalog_number.data
                                                          , form.discount_percentage.data
                                                          , request.form.get('double_deals'), form.start_date.data
                                                          , form.end_date.data)
        flash(resp.message, 'success' if resp.val else 'danger')

        # flash(form.catalog_number.data, 'success')
        # flash(form.discount_percentage.data, 'success')
        # flash(request.form.get('double_deals'), 'success')
        # flash(form.start_date.data, 'success')
        # flash(form.end_date.data, 'success')

        return redirect(url_for('add_regular_discount'))
    return render_template('add_regular_discount.html', form=form,
                           title='add regular discount policy', legend='add regular discount policy')


@app.route("/add_conditional_discount", methods=['GET', 'POST'])
def add_conditional_discount():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = AddConditionalDiscountPolicyToProduct()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().add_cond_discount(UserSessions.current_user.username
                                                          , form.first_product.data
                                                          , form.discount_percentage.data
                                                          , request.form.get('double_deals')
                                                          , form.start_date.data
                                                          , form.end_date.data
                                                          , request.form.get('or_and')
                                                          , form.second_product.data)

        flash(resp.message, 'success' if resp.val else 'danger')

        # flash(form.discount_percentage.data, 'success')
        # flash(request.form.get('double_deals'), 'success')
        # flash(form.start_date.data, 'success')
        # flash(form.end_date.data, 'success')
        # flash(form.first_product.data, 'success')
        # flash(request.form.get('or_and'), 'success')
        # flash(form.second_product.data, 'success')

        return redirect(url_for('add_conditional_discount'))
    return render_template('add_conditional _discount.html', form=form,
                           title='add conditional discount policy', legend='add conditional discount policy')


@app.route("/add_store_discount_policy", methods=['GET', 'POST'])
def add_store_discount_policy():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = AddDiscountPolicyToStore()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().add_reg_discount_of_store(UserSessions.current_user.username
                                                                  , form.store_number.data, form.discount_percentage.data
                                                                  , request.form.get('double_deals')
                                                                  , form.start_date.data
                                                                  , form.end_date.data)

        flash(resp.message, 'success' if resp.val else 'danger')

        # flash(form.store_number.data, 'success')
        # flash(form.discount_percentage.data, 'success')
        # flash(request.form.get('double_deals'), 'success')
        # flash(form.start_date.data, 'success')
        # flash(form.end_date.data, 'success')
        return redirect(url_for('add_store_discount_policy'))
    return render_template('add_store_discount_policy.html', form=form,
                           title='add store discount policy', legend='add store discount policy')


@app.route("/permanently_close", methods=['GET', 'POST'])
def permanently_close():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = PermanentlyClose()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().close_permanently(UserSessions.current_user.username, form.store_number.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('permanently_close'))
    return render_template('permanently_close.html', form=form,
                           title='Permanently Close Store', legend='Permanently Close Store')


@app.route("/add_buying_policy", methods=['GET', 'POST'])
def add_buying_policy():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = AddBuyingPolicyForm()
    if form.validate_on_submit():
        if form.submit0.data:
            return redirect(url_for('limit_quantity'))
        elif form.submit1.data:
            return redirect(url_for('limit_quantity_per_store'))
        elif form.submit2.data:
            return redirect(url_for('limit_age'))
    return render_template('add_buying_policy.html', title='Add Buying Policy',
                           legend='Add A Buying Policy:',
                           form=form)


@app.route("/add_discount_policy", methods=['GET', 'POST'])
def add_discount_policy():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = AddDiscountPolicyForm()
    if form.validate_on_submit():
        if form.submit0.data:
            return redirect(url_for('add_regular_discount'))
        elif form.submit1.data:
            return redirect(url_for('add_conditional_discount'))
        elif form.submit2.data:
            return redirect(url_for('add_store_discount_policy'))
    return render_template('add_discount_policy.html', title='Add Discount Policy',
                           legend='Add A Discount Policy:',
                           form=form)


@app.route("/product_management", methods=['GET', 'POST'])
def product_management():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = ProductManagementForm()
    if form.validate_on_submit():
        if form.submit0.data:
            return redirect(url_for('new_product'))
        elif form.submit1.data:
            return redirect(url_for('update_product_details'))
        elif form.submit2.data:
            return redirect(url_for('remove_product'))
    return render_template('product_management.html', title='Product Management',
                           legend='Please Choose An Option:',
                           form=form)


@app.route("/policies", methods=['GET', 'POST'])
def policies():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = PoliciesForm()
    if form.validate_on_submit():
        if form.submit0.data:
            return redirect(url_for('add_buying_policy'))
        elif form.submit1.data:
            return redirect(url_for('add_discount_policy'))
    return render_template('policies.html', title='Policies',
                           legend='Please Choose An Option:',
                           form=form)


@app.route("/administrator_options", methods=['GET', 'POST'])
def administrator_options():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = AdminOptionsForm()
    if form.validate_on_submit():
        if form.submit0.data:
            return redirect(url_for('remove_subscriber'))
        elif form.submit1.data:
            return redirect(url_for('permanently_close'))
    return render_template('administrator_options.html', title='Admin Options',
                           legend='Please Choose An Option:',
                           form=form)


@app.route("/limit_quantity", methods=['GET', 'POST'])
def limit_quantity():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = LimitQuantity()
    if form.validate_on_submit():
        if form.minimum_quantity.data == '' and form.maximum_quantity.data == '':
            flash('At least one of the maximum or minimum values must be filled', 'danger')
            return redirect(url_for('limit_quantity'))
        resp0 = None
        resp1 = None
        if form.minimum_quantity.data != '':
            resp0 = Ecommerce.get_instance().change_details_of_product(UserSessions.current_user.username,
                                                                       form.catalog_number.data, 'minimum_products',
                                                                       form.minimum_quantity.data)
        if form.maximum_quantity.data != '':
            resp1 = Ecommerce.get_instance().change_details_of_product(UserSessions.current_user.username,
                                                                       form.catalog_number.data, 'maximum_products',
                                                                       form.maximum_quantity.data)
        if resp0 and resp1 and resp0.val and resp1.val:
            flash(resp0.message, 'success')
        else:
            flash('Something went wrong, please check and try again', 'danger')

        return redirect(url_for('limit_quantity'))
    return render_template('limit _quantity.html', form=form, title='limit quantity', legend='limit quantity')


@app.route("/limit_age", methods=['GET', 'POST'])
def limit_age():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = LimitAge()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().change_details_of_product(UserSessions.current_user.username,
                                                                  form.catalog_number.data, 'minimum_age',
                                                                  form.minimum_age.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('limit_age'))
    return render_template('limit_age.html', form=form, title='limit age', legend='limit age')

@app.route("/limit_quantity_per_store", methods=['GET', 'POST'])
def limit_quantity_per_store():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = LimitQuantityPerStore()
    if form.validate_on_submit():
        if form.minimum_quantity.data == '' and form.maximum_quantity.data == '':
            flash('At least one of the maximum or minimum values must be filled', 'danger')
            return redirect(url_for('limit_quantity'))
        resp0 = None
        resp1 = None
        if form.minimum_quantity.data != '':
            resp0 = Ecommerce.get_instance().change_details_of_store(UserSessions.current_user.username,
                                                                     form.store_number.data, 'minimum_products',
                                                                     form.minimum_quantity.data)
        if form.maximum_quantity.data != '':
            resp1 = Ecommerce.get_instance().change_details_of_store(UserSessions.current_user.username,
                                                                     form.store_number.data, 'maximum_products',
                                                                     form.maximum_quantity.data)
        if resp0 and resp1 and resp0.val and resp1.val:
            flash(resp0.message, 'success')
        else:
            flash('Something went wrong, please check and try again', 'danger')

    return render_template('limit_quantity_per_store.html', form=form, title='limit quantity per store',
                           legend='limit quantity per store')


@app.route("/workers_management", methods=['GET', 'POST'])
def workers_management():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = WorkersManagementForm()
    if form.validate_on_submit():
        if form.submit0.data:
            return redirect(url_for('add_store_manager'))
        elif form.submit1.data:
            return redirect(url_for('add_store_owner'))
        elif form.submit2.data:
            return redirect(url_for('remove_store_manager'))
        elif form.submit3.data:
            return redirect(url_for('remove_store_owner'))
    return render_template('workers_management.html', title='Workers Management',
                           legend='Please Choose An Option:',form=form)


@app.route("/add_store_manager", methods=['GET', 'POST'])
def add_store_manager():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = AddStoreManager()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().add_store_manager(UserSessions.current_user.username, form.store_number.data,
                                                        form.username.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('add_store_manager'))
    return render_template('add_store_manager.html', form=form, title='Add Store Manager', legend='Add Store Manager')


@app.route("/add_store_owner", methods=['GET', 'POST'])
def add_store_owner():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = AddStoreOwner()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().add_store_owner(UserSessions.current_user.username, form.store_number.data,
                                                        form.username.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('add_store_owner'))
    return render_template('add_store_owner.html', form=form, title='Add Store Owner', legend='Add Store Owner')


@app.route("/remove_store_manager", methods=['GET', 'POST'])
def remove_store_manager():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = RemoveStoreManager()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().remove_store_manager(UserSessions.current_user.username, form.store_number.data,
                                                        form.username.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('remove_store_manager'))
    return render_template('remove_store_manager.html', form=form, title='Remove Store Manager', legend='Remove Store Manager')


@app.route("/remove_store_owner", methods=['GET', 'POST'])
def remove_store_owner():
    if not UserSessions.current_user.is_logged_in:
        return redirect(url_for('login'))

    form = RemoveStoreOwner()
    if form.validate_on_submit():
        resp = Ecommerce.get_instance().remove_store_owner(UserSessions.current_user.username, form.store_number.data,
                                                           form.username.data)
        flash(resp.message, 'success' if resp.val else 'danger')
        return redirect(url_for('remove_store_owner'))
    return render_template('remove_store_owner.html', form=form, title='Remove Store Owner', legend='Remove Store Owner')
