from blog.models.users import User
from blog.models.local_auth import LocalAuth
from blog.models.blogs import Blog
from blog.common.db import use_orm
from blog.common.token import Token
from blog.common.exceptions import ClientError, ErrorCode
from blog.common.utils import password_maker
from blog.common.logger import logger


class UserController:

    @classmethod
    @use_orm
    def register(cls, email, nickname, *, session):
        user = session.query(User).filter_by(email=email).first()
        if user:
            raise ClientError(code=400, err=ErrorCode.USER_EXISTS,
                              msg='该用户已经存在，请直接登录')
        with session.begin():
            new_user = User(nickname=nickname, email=email)
            session.add(new_user)
            new_user = session.query(User).filter_by(email=email).first()
            token = Token.encode(
                user_id=new_user.id, nickname=new_user.nickname)

            default_password = '0123456789'
            db_password = password_maker(default_password)
            auth = LocalAuth(user_id=new_user.id, password=db_password)
            session.add(auth)

            blog = Blog(user_id=new_user.id,name=nickname)
            session.add(blog)

        ret = {'id': new_user.id, 'nickname': new_user.nickname,
               'default_password': default_password, 'token': token}
        return ret

    @classmethod
    @use_orm
    def login(cls, email, password, *, session):
        user = session.query(User).filter_by(email=email).first()
        if not user:
            raise ClientError(code=400, err=ErrorCode.USER_NOT_FOUND,
                              msg='用户不存在')
        auth = session.query(LocalAuth).filter_by(user_id=user.id).first()
        if not auth:
            raise ClientError(code=400, err=ErrorCode.USER_NOT_FOUND,
                              msg='用户未设置密码')
        client_password = password_maker(password=password)
        if client_password != auth.password:
            raise ClientError(code=401, err=ErrorCode.PASSWORD_ERROR,
                              msg='密码错误')
        token = Token.encode(user_id=user.id, nickname=user.nickname)
        return dict(user_id=user.id, token=token, nickname=user.nickname)

    @classmethod
    @use_orm(name='ro')
    def detail(cls, user_id, *, session):
        user = session.query(User).filter_by(id=user_id).first()
        return user
