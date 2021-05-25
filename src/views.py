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


def shop_category(request, values):
    shop = Shop.get(slug=values.get('slug'))

    if shop is None:
        return NotFound()

    category = Category.get(name=values.get('category'))

    if category is None:
        return NotFound()

    products = Product.get_by_shop_category(shop.id, category.id)

    return render_template('category.html', {
        'category': category,
        'shop': shop,
        'products': products})


def product_detail(request, values):
    product = Product.get(pk=values.get('id'))

    if product is None:
        return NotFound()

    return render_template('product.html', {'product': product})


def product_delete(request, values):
    product = Product.get(pk=values.get('id'))

    if product is None:
        return NotFound()

    product.delete()
    return redirect(product.shop.get_absolute_url())


def product_create(request, values):
    shop = Shop.get(slug=values.get('slug'))

    if shop is None:
        return NotFound()

    if request.method == 'GET':
        categories = Category.all()
        return render_template('product-form.html', {'categories': categories, 'shop' : shop})

    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    categories = request.form.getlist('category')
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
        shop_id=shop.id,
        description=description)

    for category in categories:
        product.add_category(category)

    return redirect(f'/shops/{shop.slug}/products/{product.id}')


def product_update(request, values):
    shop = Shop.get(slug=values.get('slug'))
    product = Product.get(pk=values.get('id'))
    product_categories = [category.id for category in product.get_categories()]

    if shop is None or product is None:
        return NotFound()

    if request.method == 'GET':
        categories = Category.all()
        return render_template('product-form.html', {
            'categories': categories,
            'shop': shop,
            'product': product,
            'product_categories': product_categories,
        })

    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    categories = request.form.getlist('category')
    image = request.files.get('image')

    if image and image.filename != product.image:
        if allowed_image(image.filename):
            image_name = secure_filename(image.filename)
            image.save(os.path.join(MEDIA_ROOT, image_name))
            if product.image != '':
                os.remove(os.path.join(MEDIA_ROOT, product.image))
        else:
            image_name = ''
    else:
        image_name = ''

    product.update(
        name=name or product.name,
        price=price or product.price,
        description=description or product.description,
        image=image_name or product.image,
    )

    # TODO: update categories

    return redirect(f'/shops/{shop.slug}/products/{product.id}')

    # for category in categories:
    #     if category not in product_categories:
    #         product.add_category(category)


    # product = Product.create(
    #     name=name,
    #     price=price,
    #     image=image_name,
    #     shop_id=shop.id,
    #     description=description)

    # for category in categories:
    #     product.add_category(category)




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
    shop = Shop.get(slug=values.get('slug'))

    if shop is None:
        return NotFound()

    username = request.form.get('username')
    text = request.form.get('text')

    ShopReview.create(
        username=username,
        text=text,
        shop_id=shop.id)

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
