import os

from jinja2 import Environment, FileSystemLoader
from werkzeug.wrappers import Response

template_path = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = Environment(loader=FileSystemLoader(template_path))


def render_template(template_name, context=None):
    template = jinja_env.get_template(template_name)
    return Response(template.render(context or {}), mimetype='text/html')
