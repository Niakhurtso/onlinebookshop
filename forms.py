from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email,  length, equal_to


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired(), length(min=8, message="პაროლი მოკლეა")])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), equal_to("password1",
                                                                                      message="პაროლები არ ემთხვევა")])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class SearchForm(FlaskForm):
    def __init__(self, formdata=None, **kwargs):
        super().__init__(formdata, **kwargs)
        self.search_term = None

    searchBar = StringField('Search bar')
    searchButton = SubmitField('Search')


class AddBookForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    image = FileField("Image", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])
    submit = SubmitField('Add Product')



class FavoriteForm(FlaskForm):
    productId = StringField()
    addToCart = SubmitField('Add to cart')
    delete = SubmitField('delete')


class CartForm(FlaskForm):
    def __init__(self, formdata=None, **kwargs):
        super().__init__(formdata, **kwargs)
        self.quantity = None
        self.product_id = None

    productId = StringField()
    removeFromCart = SubmitField('delete')


class DeleteForm(FlaskForm):
    productId = StringField()
    addToCart = SubmitField('Add to cart')
    delete = SubmitField('delete')


class ProductForm(FlaskForm):
    productId = StringField()
    addToCart = SubmitField('Add to cart')
    favorite = SubmitField('❤')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
