import functools
import jwt
from datetime import datetime, timedelta
from flask import request

from blog.common.utils import SingletonMixin
from blog.common.logger import logger
from blog.common.exceptions import ServerError, ClientError, ErrorCode
import blog


class RsaKeyStorage(SingletonMixin):
    def __init__(self):
        self.pub_key = None
        self.pri_key = None

    def set_key_content(self, pub_key, pri_key):
        self.pub_key = pub_key
        self.pri_key = pri_key


def init_rsa_key():
    """ 初始化公私钥 """
    pub_key_route = blog.app.config['PUB_KEY_ROUTE']
    pri_key_route = blog.app.config['PRI_KEY_ROUTE']
    with open(pub_key_route) as f:
        pub_key_content = f.read()
    with open(pri_key_route) as f:
        pri_key_content = f.read()
    rsa_key_storage = RsaKeyStorage.instance()
    rsa_key_storage.set_key_content(pub_key_content, pri_key_content)


class Token:

    @classmethod
    def encode(cls, *, user_id, nickname):
        rsa_key_storage = RsaKeyStorage.instance()
        try:
            exp_seconds = int(blog.app.config['TOKEN_EXP_SECONDS'])
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=exp_seconds),
                'nbf': datetime.utcnow(),
                'ttl': exp_seconds,
                'iat': datetime.utcnow(),
                'data': {'userId': user_id, 'nickname': nickname},
                'format': 'utc',
            }
            return jwt.encode(
                payload,
                rsa_key_storage.pri_key,
                algorithm='RS256',
            )
        except Exception as e:
            logger.exception(e)
            raise ServerError(code=401, err=ErrorCode.JWT_ENCODE,
                              msg='颁发token错误')

    @classmethod
    def decode(cls, auth_token):
        rsa_key_storage = RsaKeyStorage.instance()
        try:
            payload = jwt.decode(auth_token, rsa_key_storage.pub_key,
                                 options={'verify_exp': True})
            return payload
        except jwt.ExpiredSignatureError:
            raise ClientError(code=401, err=ErrorCode.JWT_DECODE,
                              msg='登录已过期,请重新登录')
        except jwt.InvalidTokenError:
            raise ClientError(code=401, err=ErrorCode.JWT_DECODE,
                              msg='登录无效,请重新登录')


def need_login(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get('User-Token')
        if not auth_token:
            raise ClientError(code=401, err=ErrorCode.NEED_LOGIN, msg='需要登录')
        payload = Token.decode(auth_token)
        kwargs.update(user_id=int(payload['data']['userId']))
        return func(*args, **kwargs)

    return wrapper
