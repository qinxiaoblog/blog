from marshmallow import Schema, fields


class _Category(Schema):
    name = fields.String(dump_to='name', required=True)
    count = fields.Integer(dump_to='count', required=True)


class ResponseCategoryList(Schema):
    category_list = fields.Nested(_Category, dump_to='categoryList', many=True)


res_category_list = ResponseCategoryList(strict=True)