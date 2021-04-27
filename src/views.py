import os

from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect, secure_filename

from models import Category, Product, Shop, ShopReview
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

    categories = Category.all()

    return render_template('shop.html', {'shop': shop,
                                         'categories': categories})


def product_detail(request, values):
    product = Product.get(pk=values.get('id'))

    if product is None:
        return NotFound()

    return render_template('product.html', {'product': product})


def product_create(request, values):
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    categories = request.form.getlist('category')
    image = request.files.get('image')
    shop_id = request.form.get('shop_id')

    if image and allowed_image(image.filename):
        image_name = secure_filename(image.filename)
        image.save(os.path.join(MEDIA_ROOT, image_name))
    else:
        image_name = ''

    product = Product.create(
        name=name,
        price=price,
        image=image_name,
        shop_id=shop_id,
        description=description)

    for category in categories:
        product.add_category(category)

    shop = Shop.get(shop_id)
    return redirect(shop.get_absolute_url())


def shop_create(request, values):
    name = request.form.get('name')
    slug = request.form.get('slug')
    image = request.files.get('image')

    if image and allowed_image(image.filename):
        image_name = secure_filename(image.filename)
        image.save(os.path.join(MEDIA_ROOT, image_name))
    else:
        image_name = ''

    shop = Shop.create(
        name=name,
        slug=slug,
        image=image_name)

    return redirect(shop.get_absolute_url())


def shop_review_create(request, values):
    username = request.form.get('username')
    text = request.form.get('text')
    shop_id = request.form.get('shop_id')

    ShopReview.create(
        username=username,
        text=text,
        shop_id=shop_id)

    shop = Shop.get(shop_id)
    return redirect(shop.get_absolute_url())


# def shop_category_create(request, values):
#     name = request.form.get('name')
#     image = request.files.get('image')

#     if image and allowed_image(image.filename):
#         image_name = secure_filename(image.filename)
#         image.save(os.path.join(MEDIA_ROOT, image_name))
#     else:
#         image_name = ''

#     Category.create(
#         name=name,
#         image=image)

#     return redirect('/')
