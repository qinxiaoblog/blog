import os
from flask import Flask
import pike.discovery.py as discovery
from werkzeug.exceptions import NotFound

from blog.common.logger import init_logger
from blog.common import exceptions
from blog.common.exceptions import (
    handle_exception, handle_custom_exception, handle_not_found)
from blog.common.token import init_rsa_key


root_dir = os.path.join(os.path.dirname(__file__), '../')
app = application = Flask(__name__)


app.config.from_pyfile(
    os.path.join(root_dir, 'blog/settings/default_settings.py'), silent=True)
app.config.from_pyfile(os.path.join(root_dir, '.settings.py'), silent=True)
silent = True if app.config['DEBUG'] else False
app.config.from_envvar('BLOG_SETTINGS', silent=silent)


logger = init_logger('/tmp/blog.log', loglevel=app.config['LOG_LEVEL'].upper())


import blog.apps.weblog  # NOQA
import blog.apps.admin  # NOQA
app.register_blueprint(blog.apps.weblog.weblog)
app.register_blueprint(blog.apps.admin.admin)


def register_exceptions():
    app.register_error_handler(Exception, handle_exception)
    app.register_error_handler(NotFound, handle_not_found)
    for e in discovery.get_all_classes(exceptions):
        if not hasattr(e, 'custom'):
            continue
        app.register_error_handler(e, handle_custom_exception)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,User-Token')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


register_exceptions()
init_rsa_key()
