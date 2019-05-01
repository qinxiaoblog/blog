from flask import jsonify
from werkzeug.exceptions import HTTPException
from enum import Enum, unique

from blog.common.logger import logger


@unique
class ErrorCode(Enum):

    # success code
    SUCCESS = 0                              # 成功

    # These ErrorCode belongs to server, code number starts with 1
    EXCEPTION = 1                            # 内部错误(未知错误)
    SERVER = 10                              # 服务器错误(自定义错误)
    CLIENT = 11                              # 客户端错误(自定义错误)
    JWT_ENCODE = 12                          # token生成错误

    # These ErrorCode belongs to client, code number starts with 2
    METHOD_NOT_ALLOWED = 2                   # 请求方法错误
    JWT_DECODE = 21                          # token解码错误
    NEED_LOGIN = 22                          # 需要登录
    ARGS_ERROR = 23                          # 请求参数错误
    USER_EXISTS = 24                         # 用户已经存在
    USER_NOT_FOUND = 25                      # 用户不存在
    PASSWORD_ERROR = 26                      # 登录密码错误
    PAGE_NOT_FOUND = 27                      # 页面找不到
    CONTENT_TYPE_ERROR = 28                  # content type error
    CONTENT_ERROR = 29                       # content error



def handle_exception(error):
    response = dict(err=ErrorCode.EXCEPTION.name,
                    msg='Internal Exception', data=None)
    logger.exception(error)
    return jsonify(response), 500


def handle_not_found(error):
    response = dict(err=ErrorCode.PAGE_NOT_FOUND.name,
                    msg='URL not found', data=None)
    logger.exception(error)
    return jsonify(response), 404


def handle_custom_exception(error):
    response = dict(err=error.err.name, msg=error.msg, data=error.data)
    logger.exception(f'ERROR: {response}, {error}')
    return jsonify(response), error.code


class CustomException(HTTPException):
    custom = True

    def __init__(self, code=None, err=None, msg=None, data=None):
        if err is not None and not isinstance(err, ErrorCode):
            raise Exception(f'ErrorCode: {err} must be Enume type ErrorCode')
        self.code = code if code is not None else self.code
        self.err = err if err is not None else self.err
        self.msg = msg if msg is not None else self.msg
        self.data = data if data is not None else self.data


class ServerError(CustomException):
    code = 500
    err = ErrorCode.SERVER
    msg = 'Server Error'
    data = None


class ClientError(CustomException):
    code = 400
    err = ErrorCode.CLIENT
    msg = 'Client Error'
    data = None
