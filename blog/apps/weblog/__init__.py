import pike.discovery.py as discovery
from flask import Blueprint
from blog.common.logger import logger
from blog.apps.weblog import views


weblog = Blueprint('weblog', __name__, url_prefix='/api/v1')


def load_views():
    num_routes = 0
    for v in discovery.get_all_classes(views):
        if hasattr(v, 'route') and isinstance(v.route, str):
            logger.info(f'Adding route {v.route} from {v.__name__} ...')
            weblog.add_url_rule(v.route,
                                view_func=v.as_view(v.__name__.lower()))
            num_routes += 1
    logger.info(f'# {num_routes} routes has been successfully added.')


load_views()
