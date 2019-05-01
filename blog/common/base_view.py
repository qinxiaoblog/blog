from flask.views import MethodView

from blog.common.exceptions import ClientError, ErrorCode


class BaseView(MethodView):

    def get(self, *args, **kwargs):
        raise ClientError(
            code=405, err=ErrorCode.METHOD_NOT_ALLOWED,
            msg='Method(GET) Not Allowed!', data=None)

    def put(self, *args, **kwargs):
        raise ClientError(
            code=405, err=ErrorCode.METHOD_NOT_ALLOWED,
            msg='Method(PUT) Not Allowed!', data=None)

    def post(self, *args, **kwargs):
        raise ClientError(
            code=405, err=ErrorCode.METHOD_NOT_ALLOWED,
            msg='Method(POST) Not Allowed!', data=None)

    def delete(self, *args, **kwargs):
        raise ClientError(
            code=405, err=ErrorCode.METHOD_NOT_ALLOWED,
            msg='Method(DELETE) Not Allowed!', data=None)

    def patch(self, *args, **kwargs):
        raise ClientError(
            code=405, err=ErrorCode.METHOD_NOT_ALLOWED,
            msg='Method(PATCH) Not Allowed!', data=None)
