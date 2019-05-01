import threading
import hashlib
from blog.common.exceptions import ServerError
from blog.common.logger import logger


class SingletonMixin:

    __instance_lock = threading.Lock()

    @classmethod
    def instance(cls):
        if not hasattr(cls, '__instance'):
            with cls.__instance_lock:
                if not hasattr(cls, '__instance'):
                    logger.debug(f"create a singleton instance for '{cls}'")
                    setattr(cls, '__instance', cls())
        return getattr(cls, '__instance')


def password_maker(password):
    if not isinstance(password, str):
        raise ServerError('passwd format error')
    return hashlib.md5(password.encode()).hexdigest()
