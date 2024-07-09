from os import path

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from app import app
from ext import db
from forms import SignupForm, LoginForm, AddBookForm, SearchForm, CartForm
from models import Product, User, Cart

profiles = []

books = [
    {
        "image": "https://apiv1.biblusi.ge/storage/book/z7y89eGQUxvDXn1QHwn2s3ed4MxyVdGq2jdcz5fM.jpg",
        "id": 1,
        "title": "პროცესი",
        "author": "ფრანც კაფკა",
        "price": "9,90"
    },

    {
        "image": "https://apiv1.biblusi.ge/storage/book/QgNCjCr2ipwF0XtrzRmeMXx2TJVQTkBkFeNOkqT1.jpg",
        "id": 2,
        "title": "ნუ მოკლავ ჯაფარას",
        "author": "ჰარპერ ლი",
        "price": "14,90"
    },

    {
        "image": "https://api.palitral.ge/storage/upload/image-png/2024-03-12/moswavlis_archevani_javaxishvili_4e65574ca1e6f925fa530ac7f26a38fa.png.webp",
        "id": 3,
        "title": "ჯაყოს ხიზნები",
        "author": "მიხეილ ჯავახიშვილი",
        "price": "17,90"
    },

    {
        "image": "https://api.palitral.ge/storage/book/n7x8sjhetFZrfmpMMELrVktAthkgYbtEcgx1PpkB.png.webp",
        "id": 4,
        "title": "1984",
        "author": "ჯორჯ ორუელი",
        "price": "15,90"
    },

    {
        "image": "https://api.palitral.ge/storage/book/acuKX8566l6BZ3KvirJnB8RY6CCkaerH8z39AYpH.png.webp",
        "id": 5,
        "title": "ცხოველების ფერმა",
        "author": "ჯორჯ ორუელი",
        "price": "10,95"
    },

    {
        "image": "https://i0.wp.com/www.sulakauri.ge/wp-content/uploads/2022/05/patara-printsi.webp?w=600&ssl=1",
        "id": 6,
        "title": "პატარა პრინცი",
        "author": "ანტუან დე სენტ-ეგზიუპერი",
        "price": "8,90"
    },

    {
        "image": "https://i0.wp.com/www.sulakauri.ge/wp-content/uploads/2020/02/mur-norvegiuli-tqhe.jpg?w=600&ssl=1",
        "id": 7,
        "title": "ნორვეგიული ტყე",
        "author": "ჰარუკი მურაკამი",
        "price": "17,90"
    },

    {
        "image": "https://i0.wp.com/www.sulakauri.ge/wp-content/uploads/2022/08/patara-qalebi.webp?w=504&ssl=1",
        "id": 8,
        "title": "პატარა ქალები",
        "author": "ლუიზა მეი ოლკოტი",
        "price": "15,90"
    },


    {
        "image": "https://api.palitral.ge/storage/upload/image-png/2024-03-12/sagizheti_486d0de0c9e42b1624fa43a0fda2f7fc.png.webp",
        "id": 9,
        "title": "საგიჟეთი",
        "author": "მედლინ რუ",
        "price": "12,95"
    },

    {
        "image": "https://api.palitral.ge/storage/upload/image-png/2021-12-49/dante-alig-200x260-2_(1)_84c9d9ffa5ea3e7ff687c18446310772.png.webp",
        "id": 10,
        "title": "ღვთაებრივი კომედია",
        "author": "დანტე ალეგიერი",
        "price": "23,95"
    },

    {
        "image": "https://api.palitral.ge/storage/upload/image-png/2023-09-37/kacia-adamiani_f45029ae7d338d67c0e249bae31a4be4.png.webp",
        "id": 11,
        "title": "კაცია ადამიანი ?!",
        "author": "ილია ჭავჭავაძე",
        "price": "22,90"
    },

    {
        "image": "https://i0.wp.com/www.sulakauri.ge/wp-content/uploads/2022/11/kaphka-plazhze.webp?w=600&ssl=1",
        "id": 12,
        "title": "კაფკა პლაჟზე",
        "author": "ჰარუკი მურაკამი",
        "price": "18,90"
    },

    {
        "image": "https://apiv1.biblusi.ge/storage/book/fqs18Hgk2mXp1mjxo43p0WGzk3Fs69COM4bdbIlT.jpg",
        "id": 13,
        "title": "გარდასახვა",
        "author": "ფრანც კაფკა",
        "price": "9,95"
    },

    {
        "image": "https://apiv1.biblusi.ge/storage/book/syK49WIW2waquuKDTfz2MSBisMUUceVOGutV2YVR.jpg",
        "id": 14,
        "title": "ფრანით მორბენალი",
        "author": "ხალიდ ჰოსეინი",
        "price": "15,95"
    },

    {
        "image": "https://apiv1.biblusi.ge/storage/book/OjDyUnMM2JFUxNF4biopPMlusY9iiGHiLL0OMpl0.png",
        "id": 15,
        "title": "ზებულონი",
        "author": "ჯემალ ქარჩხაძე",
        "price": "19,95"
    },

    {
        "image": "https://apiv1.biblusi.ge/storage/book/PVUrpO0LbLAyabVPzagZUAXoS218GMjOvwxJxbse.jpg",
        "id": 16,
        "title": "მზე, მთვარე და პურის ყანა",
        "author": "თემურ ბაბლუანი",
        "price": "19,95"
    },

    {
        "image": "https://apiv1.biblusi.ge/storage/book/SsPqeubHAP9bR2NrGgn7kRAkTjReZROdYjWtdMqe.jpg",
        "id": 17,
        "title": "შაშვი შაშვი მაყვალი",
        "author": "თამთა მელაშვილი",
        "price": "14,95"
    },

    {
        "image": "https://apiv1.biblusi.ge/storage/book/OsE65lBJ9gI06ma9y4fMGEpP1Ws89iGBUbdSvci3.jpg",
        "id": 18,
        "title": "დიდოსტატის მარჯვენა",
        "author": "კონსტანტინე გამსახურდია",
        "price": "16,95"
    },

    {
        "image": "https://api.palitral.ge/storage/upload/image-png/2022-03-13/Untitled-1_(4)_406add4b375a10c2d56857e5db2ee514.png.webp",
        "id": 19,
        "title": "ჯეინ ეარი - Jane eyre",
        "author": "შარლოტა ბრონტე",
        "price": "11,95"
    },

    {
        "image": "https://i0.wp.com/www.sulakauri.ge/wp-content/uploads/2020/07/natsqhvdiadevs_600.jpg?w=600&ssl=1",
        "id": 20,
        "title": "ნაწყვდიადევს",
        "author": "ჯოზეფ კონრადი",
        "price": "10,95"
    },

    {
        "image": "https://api.palitral.ge/storage/book/TsL452prgpXr8S34hY9Eu6PsZu8doUOFKLRo2muW.png.webp",
        "id": 21,
        "title": "ფეხებზე დაკიდების ნატიფი ხელოვნება",
        "author": "მარკ მენსონი ",
        "price": "16,95"
    },

    {
        "image": "https://api.palitral.ge/storage/upload/image-png/2022-01-04/18_%E1%83%A1%E1%83%94%E1%83%A0%E1%83%95%E1%83%90%E1%83%9C%E1%83%A2%E1%83%94%E1%83%A1%E1%83%98_-_%E1%83%93%E1%83%9D%E1%83%9C_%E1%83%99%E1%83%98%E1%83%AE%E1%83%9D%E1%83%A2%E1%83%98_1_306f010baa3549635443331d33162d24.png.webp",
        "id": 22,
        "title": "დონ კიხოტი ნაწ.1",
        "author": "მიგელ დე სერვანტესი",
        "price": "16,95"
    },

    {
        "image": "https://api.palitral.ge/storage/upload/image-png/2021-12-50/9789941322365_(1)_5ba2e6810bdb69caa69f1b02f91e088f.png.webp",
        "id": 23,
        "title": "the great gatsby",
        "author": "F. Scott Fitzgerald",
        "price": "11,95"
    }
]

@app.route('/')
def home():
    search_form = SearchForm()

    if search_form.validate_on_submit():
        search_query = search_form.searchBar.data
        products = Product.query.filter(Product.name.ilike(f"%{search_query}%")).all()
    else:
        products = Product.query.all()


    return render_template('home.html', products=products, search_form=search_form)


@app.route('/products')
@login_required
def product_list():
    search_form = SearchForm()
    products = Product.query.all()
    return render_template('product.html', products=products, search_form=search_form)


@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_product():
    search_form = SearchForm()
    form = AddBookForm()
    if form.validate_on_submit():
        print("here")
        image = form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)
        new_product = Product(name=form.name.data, description=form.description.data, price=form.price.data, img=image.filename)

        db.session.add(new_product)
        db.session.commit()


        return redirect(url_for('product_list'))
    return render_template('add_book.html', form=form, search_form=search_form)




@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        search_term = form.search_term.data
        results = Product.query.filter(Product.name.contains(search_term)).all()
        if not results:
            flash('No products found.')
    return render_template('search.html', form=form, results=results, search_form=search_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    search_form = SearchForm()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form, search_form=search_form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    search_form = SearchForm()
    if signup_form.validate_on_submit():

        if User.query.filter_by(username=signup_form.username.data).first():
            flash('Username is already in use', 'danger')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=signup_form.email.data).first():
            flash('Email is already in use', 'danger')
            return redirect(url_for('signup'))

        new_user = User(username=signup_form.username.data, email=signup_form.email.data,
                        password=signup_form.password1.data, is_admin=True)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', signup_form=signup_form, search_form=search_form)


@app.route('/logout')
@login_required
def logout():
    search_form = SearchForm()
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('home'))

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    search_form = SearchForm()
    form = CartForm()
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        if product:
            cart_item = Cart(user_id=current_user.id, product_id=product.id, quantity=form.quantity.data)
            db.session.add(cart_item)
            db.session.commit()
            flash('Product added to cart.')
        else:
            flash('Product not found.')
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', form=form, cart_items=cart_items, search_form=search_form)

@app.route('/cart/remove/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    search_form = SearchForm()
    cart_item = Cart.query.get(item_id)
    if cart_item and cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart.')
    else:
        flash('Item not found.')
    return redirect(url_for('cart'))


@app.route('/about')
def about():
    search_form = SearchForm()
    return render_template('about.html', search_form=search_form)


@app.route('/books')
def books_view():
    search_form = SearchForm()
    products = Product.query.all()
    return render_template('books.html', products=products, search_form=search_form)


@app.route('/contact')
def contact():
    search_form = SearchForm()
    return render_template('contact.html', search_form=search_form)


@app.route('/faq')
def faq():
    search_form = SearchForm()
    return render_template('faq.html', search_form=search_form)


@app.route('/wishlist')
@login_required
def wishlist():
    search_form = SearchForm()
    return render_template('favourite.html', search_form=search_form)

@app.route('/favourite')
def favourite():
    search_form = SearchForm()
    return render_template('favourite.html', search_form=search_form)

