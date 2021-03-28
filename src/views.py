from werkzeug.wrappers import Response


def index(request, values):
    return Response('''
    <h1><strong>Welcome to our shop!</strong></h1>
    <ul>
      <li><a href="/cart">Cart</a></li>
      <li><a href="/products/cats">Cats</a></li>
    </ul>
    ''',
                    mimetype='text/html')


def cart(request, values):
    return Response('<h1>This is a cart page!</h1>', mimetype='text/html')


def product_detail(request, values):
    return Response(f'This is a page for product {values.get("id")}',
                    mimetype='text/html')
