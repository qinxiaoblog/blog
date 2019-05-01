from marshmallow import fields, Schema


class RequestUserRegister(Schema):
    email = fields.Email(load_from='email', required=True)
    nickname = fields.String(load_from='nickname', required=True)


class ResponseUserRegister(Schema):
    id = fields.Integer(dump_to='userId')
    email = fields.Email(dump_to='email')
    nickname = fields.String(dump_to='nickname')
    token = fields.String(dump_to='token')
    default_password = fields.String(dump_to='defaultPassword')


class ResponseUserData(Schema):
    id = fields.Integer(dump_to='userId')
    nickname = fields.String(default='', dump_to='nickname')
    email = fields.Email(dump_to='email')
    description = fields.String(dump_to='description', default='')
    about_me = fields.String(dump_to='aboutMe', default='')


class RequestUserLogin(Schema):
    email = fields.Email(load_from='account', required=True)
    password = fields.String(load_from='password', required=True)


class ResponseUserLogin(Schema):
    user_id = fields.Integer(dump_to='userId')
    token = fields.String(dump_to='token')
    nickname = fields.String(dump_to='nickname')


req_user_register = RequestUserRegister(strict=True)
res_user_register = ResponseUserRegister(strict=True)

res_user_data = ResponseUserData(strict=True)

req_user_login = RequestUserLogin(strict=True)
res_user_login = ResponseUserLogin(strict=True)
