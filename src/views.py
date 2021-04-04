from db import db
from utils import render_template


def index(request, values):
    products = db.get_products()
    print(products)
    return render_template('index.html', {'products': products})


def cart(request, values):
    return render_template('cart.html')


def product_detail(request, values):
    return render_template('product.html', {'product': values.get('id')})
