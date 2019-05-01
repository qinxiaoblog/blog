from blog.common.base_view import BaseView
from blog.apps.weblog.controllers.user import UserController
from blog.apps.weblog.schemas.user import (
    req_user_register, res_user_register,
    res_user_data,
    req_user_login, res_user_login)
from blog.common.exceptions import ClientError, ErrorCode
from blog.common.schema import schema
from blog.common.token import need_login


class UserRegister(BaseView):
    route = '/user/register'

    @schema(json=req_user_register, reply=res_user_register)
    def post(self, *, json):
        """ 注册用户 """
        data = UserController.register(json['email'], json['nickname'])
        return dict(data=data)


class UserLogin(BaseView):
    route = '/user/login'

    @schema(json=req_user_login, reply=res_user_login)
    def post(self, *, json):
        """ 用户登录 """
        data = UserController.login(json['email'], json['password'])
        return dict(data=data)


class UserData(BaseView):
    route = '/user/<int:info_user_id>'

    @schema(reply=res_user_data)
    @need_login
    def get(self, **kwargs):
        if kwargs['info_user_id'] != kwargs['user_id']:
            raise ClientError(code=401, err=ErrorCode.NEED_LOGIN, msg='未登录')
        data = UserController.detail(kwargs['user_id'])
        return dict(data=data)
