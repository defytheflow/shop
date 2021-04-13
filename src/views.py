import os

from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect, secure_filename

from db import db
from settings import MEDIA_ROOT
from utils import render_template

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')


def allowed_image(image_name):
    for extension in ALLOWED_EXTENSIONS:
        if image_name.endswith(extension):
            return True
    return False


def index(request, values):
    products = db.get_products()
    print(products)
    return render_template('index.html', {'products': products})


def cart(request, values):
    return render_template('cart.html')


def product_detail(request, values):
    product = db.get_product(pk=values.get('id'))

    if product is None:
        return NotFound()

    print(product)
    return render_template('product.html', {'product': product})


def product_create(request, values):
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    image = request.files.get('image')

    if image and allowed_image(image.filename):
        image_name = secure_filename(image.filename)
        image.save(os.path.join(MEDIA_ROOT, image_name))
    else:
        image_name = ''

    db.create_product(name=name, price=price, image=image_name,
                      description=description)
    return redirect('/')
