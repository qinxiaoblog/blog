import functools
from marshmallow import Schema
from flask import jsonify, request
import ujson
from marshmallow.exceptions import ValidationError

from blog.common.exceptions import ClientError, ErrorCode
from blog.common.logger import logger


def schema(func=None, query=None, form=None, json=None, reply=None):
    if func is None:
        return functools.partial(
            schema, query=query, form=form, json=json, reply=reply)

    def try_load(s, data):
        try:
            return s.load(data).data
        except ValidationError as e:
            logger.exception(e)
            raise ClientError(code=400, err=ErrorCode.ARGS_ERROR,
                              msg=e.normalized_messages())

    def load_query(s):
        data = request.args.to_dict()
        return try_load(s, data)

    def load_form(s):
        data = request.form.to_dict()
        return try_load(s, data)

    def load_json(s):
        content_type = request.headers.get('Content-Type')
        if not content_type or not content_type.startswith('application/json'):
            raise ClientError(code=400, err=ErrorCode.CONTENT_TYPE_ERROR,
                              msg='invalid content-type')
        try:
            data = ujson.loads(request.data)
        except Exception as e:
            logger.exception(e)
            raise ClientError(code=400, err=ErrorCode.CONTENT_ERROR,
                              msg='invalid content format')
        return try_load(s, data)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        if query and isinstance(query, Schema):
            kwargs.update(query=load_query(query))
        if form and isinstance(form, Schema):
            kwargs.update(form=load_form(form))
        if json and isinstance(json, Schema):
            kwargs.update(json=load_json(json))

        ret_val = func(*args, **kwargs)
        ret_val = {} if ret_val is None else ret_val
        err = ret_val.get('err', ErrorCode.SUCCESS.name)
        msg = ret_val.get('msg', '')
        data = ret_val.get('data', None)
        if reply is not None and isinstance(reply, Schema):
            data = reply.dump(ret_val.get('data')).data

        resp = jsonify(dict(err=err, msg=msg, data=data))
        return resp

    return wrapper
