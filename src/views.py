import os

from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect, secure_filename

from models import Product, Shop
from settings import MEDIA_ROOT
from utils import render_template

ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')


def allowed_image(image_name):
    for extension in ALLOWED_EXTENSIONS:
        if image_name.endswith(extension):
            return True
    return False


def index(request, values):
    shops = Shop.all()
    return render_template('index.html', {'shops': shops})


def cart(request, values):
    return render_template('cart.html')


def shop_detail(request, values):
    shop = Shop.get(slug=values.get('slug'))

    if shop is None:
        return NotFound()

    return render_template('shop.html', {'shop': shop})


def product_detail(request, values):
    product = Product.get(pk=values.get('id'))

    if product is None:
        return NotFound()

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

    product = Product.create(
        name=name,
        price=price,
        image=image_name,
        shop_id=1,
        description=description)

    print(product)
    return redirect('/')
