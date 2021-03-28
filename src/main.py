import os

from werkzeug.exceptions import HTTPException
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request

import views

url_map = Map([
    Rule('/', endpoint='index'),
    Rule('/cart/', endpoint='cart'),
    Rule('/products/<id>/', endpoint='product_detail')
])


def dispatch_request(request):
    adapter = url_map.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        view_func = getattr(views, endpoint)
        return view_func(request, values)
    except HTTPException as err:
        return err


def application(environ, start_response):
    request = Request(environ)
    response = dispatch_request(request)
    return response(environ, start_response)


application = SharedDataMiddleware(
    application, {'': os.path.join(os.path.dirname(__file__), 'static')})

if __name__ == '__main__':
    run_simple('127.0.0.1',
               5000,
               application,
               use_debugger=True,
               use_reloader=True)
