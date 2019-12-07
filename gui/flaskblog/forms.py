from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=120)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    attribute = SelectField('Attribute', choices=[('Name', 'Name'), ('Category', 'Category'), ('Keyword', 'Keyword')])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Search')


class PurchaseForm(FlaskForm):
    card_number = IntegerField('card_number', validators=[DataRequired()])
    month = IntegerField('month', )
    year = IntegerField('year', )
    holder = StringField('holder', )
    cvv = IntegerField('cvv', )
    street = StringField('street', )
    city = StringField('city', )
    country = StringField('country',)
    zip = IntegerField('zip',)
    age = IntegerField('age')
    submit = SubmitField('Buy')


class NewProductForm(FlaskForm):
    store_number = IntegerField('Store Number', validators=[NumberRange(min=0)])
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[NumberRange(min=0)])
    amount = IntegerField('Amount', validators=[NumberRange(min=0)])
    category = StringField('Category', validators=[DataRequired()])
    keywords = StringField('Keywords (separated by spaces)', validators=[DataRequired()])
    submit = SubmitField('Create')


class UpdateDetailsForm(FlaskForm):
    catalog_number = IntegerField('Catalog Number', validators=[NumberRange(min=0)])
    attribute = SelectField('Attribute', choices=[('Name', 'Name'), ('Category', 'Category'),
                                                  ('Price', 'Price'), ('Amount', 'Amount')])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Update')


class NewStoreForm(FlaskForm):
    store_name = StringField('Store Name', validators=[DataRequired()])
    account_number = IntegerField('Account Number', validators=[NumberRange(min=0)])
    submit = SubmitField('Open Store')


class AddToCartForm(FlaskForm):
    store_number = IntegerField('Store Number', validators=[NumberRange(min=0)])
    catalog_number = IntegerField('Catalog Number', validators=[NumberRange(min=0)])
    submit = SubmitField('Add To Cart')


class RemoveFromCartForm(FlaskForm):
    store_number = IntegerField('Store Number', validators=[NumberRange(min=0)])
    catalog_number = IntegerField('Catalog Number', validators=[NumberRange(min=0)])
    submit = SubmitField('Remove From Cart')


class RemoveSubscriberForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Remove')


class RemoveProductForm(FlaskForm):
    catalog_number = IntegerField('Catalog Number', validators=[NumberRange(min=0)])
    submit = SubmitField('Remove Product')


class ShowStoreForm(FlaskForm):
    store_number = IntegerField('Store Number', validators=[NumberRange(min=0)])
    submit = SubmitField('Show Store')


class CloseStoreForm(FlaskForm):
    store_number = IntegerField('Store Number', validators=[NumberRange(min=0)])
    submit = SubmitField('Close Store')


class AddRegularDiscountPolicyToProduct(FlaskForm):
    catalog_number = StringField('catalog_number', validators=[DataRequired()])
    discount_percentage = StringField('discount_percentage', validators=[DataRequired()])
    double_deals = StringField('double_deals', validators=[DataRequired()])
    start_date = StringField('start_date', validators=[DataRequired()])
    end_date = StringField('end_date', validators=[DataRequired()])
    submit = SubmitField('Add Discount Policy')


class AddConditionalDiscountPolicyToProduct(FlaskForm):
    discount_percentage = StringField('discount_percentage', validators=[DataRequired()])
    double_deals = StringField('double_deals', validators=[DataRequired()])
    start_date = StringField('start_date', validators=[DataRequired()])
    end_date = StringField('end_date', validators=[DataRequired()])
    first_product = StringField('first_product', validators=[DataRequired()])
    or_and = StringField('or_and', validators=[DataRequired()])
    second_product = StringField('second_product', validators=[DataRequired()])
    submit = SubmitField('Add Discount Policy')


class AddDiscountPolicyToStore(FlaskForm):
    store_number = StringField('store_number', validators=[DataRequired()])
    discount_percentage = StringField('discount_percentage', validators=[DataRequired()])
    double_deals = StringField('double_deals', validators=[DataRequired()])
    start_date = StringField('start_date', validators=[DataRequired()])
    end_date = StringField('end_date', validators=[DataRequired()])
    submit = SubmitField('Add Discount Policy')


class PermanentlyClose(FlaskForm):
    store_number = IntegerField('Store Number', validators=[NumberRange(min=0)])
    submit = SubmitField('Close')


class AddBuyingPolicyForm(FlaskForm):
    submit0 = SubmitField('Limit Quantity Per Product')
    submit1 = SubmitField('Limit Quantity Per Store')
    submit2 = SubmitField('Limit Age')


class AddDiscountPolicyForm(FlaskForm):
    submit0 = SubmitField('Add Regular Discount')
    submit1 = SubmitField('Add Conditional Discount')
    submit2 = SubmitField('Add Store Discount')


class ProductManagementForm(FlaskForm):
    submit0 = SubmitField('Add New Product')
    submit1 = SubmitField('Update Product Details')
    submit2 = SubmitField('Remove Product')


class PoliciesForm(FlaskForm):
    submit0 = SubmitField('Add Buying Policy')
    submit1 = SubmitField('Add Discount Policy')


class AdminOptionsForm(FlaskForm):
    submit0 = SubmitField('Remove Subscriber')
    submit1 = SubmitField('Permanently Close Store')


class LimitQuantity(FlaskForm):
    catalog_number = StringField('catalog_number')
    minimum_quantity = StringField('minimum_quantity')
    maximum_quantity = StringField('maximum_quantity')
    submit = SubmitField('Add Buying Policy')


class LimitAge(FlaskForm):
    catalog_number = StringField('catalog_number', validators=[DataRequired()])
    minimum_age = StringField('minimum_age', validators=[DataRequired()])
    submit = SubmitField('Add Buying Policy')


class LimitQuantityPerStore(FlaskForm):
    store_number = StringField('store_number', validators=[DataRequired()])
    minimum_quantity = StringField('minimum_quantity')
    maximum_quantity = StringField('maximum_quantity')
    submit = SubmitField('Add Buying Policy')


class ShowCartForm(FlaskForm):
    store_number = IntegerField('Store Number', validators=[NumberRange(min=0)])
    submit = SubmitField('Show Cart')


class WorkersManagementForm(FlaskForm):
    submit0 = SubmitField('Add Store Manager')
    submit1 = SubmitField('Add Store Owner')
    submit2 = SubmitField('Remove Store Manager')
    submit3 = SubmitField('Remove Store Owner')


class CartManagementForm(FlaskForm):
    submit0 = SubmitField('Add To Cart')
    submit1 = SubmitField('Remove From Cart')


class AddStoreManager(FlaskForm):
    store_number = StringField('store_number', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('Add Store Manager')


class AddStoreOwner(FlaskForm):
    store_number = StringField('store_number', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('Add Store Owner')


class RemoveStoreManager(FlaskForm):
    store_number = StringField('store_number', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('Remove Store Manager')


class RemoveStoreOwner(FlaskForm):
    store_number = StringField('store_number', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('Remove Store Owner')



