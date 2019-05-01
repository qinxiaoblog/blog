import redis
from blog import app
import functools


rw_pool = redis.ConnectionPool.from_url(app.config['REDIS_RW'])
rw_conn = redis.StrictRedis(connection_pool=rw_pool)

ro_pool = redis.ConnectionPool.from_url(app.config['REDIS_RO'])
ro_conn = redis.StrictRedis(connection_pool=ro_pool)


def use_redis(func=None, name='rw'):
    if func is None:
        return functools.partial(use_redis, name=name)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if name not in ('rw', 'ro'):
            raise Exception(f'redis connection name not found: {name}')
        redis_conn = rw_conn if name == 'rw' else ro_conn
        kwargs.update(redis=redis_conn)
        ret_val = func(*args, **kwargs)
        return ret_val

    return wrapper
